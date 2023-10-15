from pulp import *
from test import *
from validation import *
from helper import *
from constants import *


def maximin_utility(file_path):

    help("Finding utility for file: " + file_path)

    ass_renters_list = []
    ass_room_list = []
    ass_rents_list = []

    values = read_preference_csv(file_path)

    # Assumption: agent list and room list are a same set
    agent_list = list(range(0, len(values[0])))
    room_list = list(range(0, len(values[0])))

    # failure(agent_list)

    if not validate_values(values):
        failure(
            "Error in Validation! Check for equal sum of each row and negative values."
        )
        return None

    # First, find a welfare-maximizing allocation
    allocation = welfare_maximize(values, agent_list, room_list)

    # Now, find envy-free rent prices
    prices = envy_free_prices(values, agent_list, room_list, allocation)

    if prices is None:
        # prices = maximinPrices(values, agent_list, room_list, allocation, rent, False)
        # if prices is None:
        failure("Failure! Prices are None!")
        return

    for agent in sorted(agent_list):
        room = allocation[agent]
        price = prices[room]
        ass_room_list.append(room + 1)
        ass_renters_list.append(agent + 1)
        ass_rents_list.append(price)
        success(f"{agent+1} {room+1} {price}")

    # Testing done here itself
    test_for_envy(ass_room_list, ass_renters_list, ass_rents_list, allocation, values)

    return ass_room_list, ass_renters_list, ass_rents_list


def welfare_maximize(values, agent_list, room_list):

    allocation = {}
    variables = {}

    # failure(agent_list)
    # failure(room_list)
    # failure(values)

    prob = LpProblem("Welfare_Maximization", LpMaximize)
    for a in agent_list:
        variables[a] = {}
        for r in room_list:
            variables[a][r] = LpVariable(f"x_{a}_{r}", 0, 1, LpBinary)

    # Objective is total welfare
    prob += lpSum(values[a][r] * variables[a][r] for a in agent_list for r in room_list)

    # Each agent assigned 1 room
    for a in agent_list:
        prob += lpSum(variables[a][r] for r in room_list) == 1

    # Each room assigned 1 agent
    for r in room_list:
        prob += lpSum(variables[a][r] for a in agent_list) == 1

    try:
        # print(prob)
        # Silence PuLP messages
        prob.solve(PULP_CBC_CMD(msg=False))
    except:
        failure("Error occured! Couldn't solve the LP problem!")
        return

    # Check the status of the solution
    if LpStatus[prob.status] != OPTIMAL:
        failure("Problem solving the LP!\t" + LpStatus[prob.status])
        return

    # Get the allocation
    for a in agent_list:
        for r in room_list:
            if variables[a][r].value() == 1:
                allocation[a] = r

    return allocation


def envy_free_prices(values, agent_list, room_list, allocation):

    prices = {}
    price_variables = {}
    rev_allocation = {y: x for x, y in allocation.items()}

    # Calculate the rent from the first row values
    rent = calculate_rent(values[0])

    prob = LpProblem("Envy_Freeness", LpMinimize)

    for r in room_list:
        # lower limit could be negative as well
        # If it is 0 then it is not a maximin utility solution
        price_variables[r] = LpVariable(
            f"p_{r}", -1 * rent, values[rev_allocation[r]][r]
        )

    # Objective is maximize minimum utility (or minimize negative of minimum utility)
    min_utility = LpVariable("y", 0)
    prob += min_utility

    # Ensure prices sum to rent
    prob += lpSum(price_variables[r] for r in room_list) == rent

    # print(agent_list, values, allocation)
    # Ensure envy-free
    for i in agent_list:
        for j in room_list:
            # Sample Envy example:
            # 12,0,0
            # 12,0,0
            # 3,5,4
            # For envyness uncomment below 2 lines
            # if i == j:
            #     continue
            prob += (
                price_variables[j] - price_variables[allocation[i]]
                >= values[i][j] - values[i][allocation[i]]
            )

    # Bound minimum utility
    for i in agent_list:
        prob += min_utility >= values[i][allocation[i]] - price_variables[allocation[i]]

    try:
        # print(prob)
        prob.solve(PULP_CBC_CMD(msg=False))
    except:
        failure("Error occured! Couldn't solve the LP problem!")
        return

    # print(agent_list, room_list, LpStatus[prob.status])

    if LpStatus[prob.status] != OPTIMAL:
        failure("Problem solving the LP!\t" + LpStatus[prob.status])
        return None

    for i in agent_list:
        room = allocation[i]
        prices[room] = price_variables[room].value()

    return prices
