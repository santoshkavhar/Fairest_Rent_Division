from pulp import *
from test import *
from validation import *
from helper import *
from constants import *


def maximin_utility(file_path, API, normalised):

    help("Finding utility for file: " + file_path)

    ass_renters_list = []
    ass_room_list = []
    ass_rents_list = []

    values, rent, capacity = read_preference_csv(file_path, API, normalised)

    # Assumption: agent list and room list are a same set
    # [[2, 0], [1, 1], [2, 0]]  means 3 agents and 2 rooms or floors
    agent_list = list(range(0, len(values)))
    room_list = list(range(0, len(values[0])))

    # failure(agent_list)
    
    if API == ROOM_API and not validate_values(values):
        failure(
            "Error in Validation! Check for equal sum of each row and negative values."
        )
        return None

    # First, find a welfare-maximizing allocation
    print("Values  in maximin utility")
    warning(values)
    warning(agent_list)
    warning(room_list)

    # Handle capacity
    if API == ROOM_API:
        capacity = [1] * 100
    allocation = welfare_maximize(values, agent_list, room_list, capacity)
    print("Allocation")
    success(allocation)
    if allocation is None:
        failure("Error in allocation")
        return
    # Trim down the agent list
    new_agent_list = list(allocation.keys())
    success(new_agent_list)

    new_room_list = list(allocation.values())
    success(new_room_list)

    # Now, find envy-free rent prices
    prices = envy_free_prices(values, new_agent_list, new_room_list, allocation)

    if prices is None:
        # prices = maximinPrices(values, agent_list, room_list, allocation, rent, False)
        # if prices is None:
        failure("Failure! Prices are None!")
        return

    for agent in sorted(new_agent_list):
        room = allocation[agent]
        price = prices[room]
        ass_room_list.append(room + 1)
        ass_renters_list.append(agent + 1)
        ass_rents_list.append(price)
        success(f"{agent+1} {room+1} {price}")


    # Normalize only if it is hostel API
    if API == HOSTEL_API:
        ass_rents_list = normalize_final_rent(ass_rents_list, rent)
    # Testing done here itself
    test_for_envy(ass_room_list, ass_renters_list, ass_rents_list, allocation, values)

    success(ass_renters_list)
    success(ass_room_list)
    success(ass_rents_list)
    return ass_room_list, ass_renters_list, ass_rents_list


def welfare_maximize(values, agent_list, room_list, capacity):

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
        prob += lpSum(variables[a][r] for r in room_list) <= 1

    # Each room assigned 1 agent
    # For floor assigned capacity agents for that floor
    for r in room_list:
        # Default capacity is 1
        prob += lpSum(variables[a][r] for a in agent_list) <= capacity[r]

    try:
        print(prob)
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
    success(allocation)
    return allocation

# floor_list is the same as room_list
def envy_free_prices(values, agent_list, room_list, allocation):

    prices = {}
    price_variables = {}
    rev_allocation = {y: x for x, y in allocation.items()}

    # Calculate the rent from the first row values
    rent = calculate_rent(values[0])

    prob = LpProblem("Envy_Freeness", LpMinimize)
    warning(room_list)
    warning(agent_list)
    warning(allocation)
    warning("values")
    warning(values)
    warning(rev_allocation)

    for r in room_list:
        # warning(values[rev_allocation[a]][a])
        # lower limit could be negative as well
        # If it is 0 then it is not a maximin utility solution
        price_variables[r] = LpVariable(
        f"p_{r}", -1 * rent, values[rev_allocation[r]][r]
        )

    # Objective is maximize minimum utility (or minimize negative of minimum utility)
    min_utility = LpVariable("y", 0)
    prob += min_utility

    warning(price_variables)
    # Ensure prices sum to rent
    prob += lpSum(price_variables[r] for r in room_list) == rent

    # print(agent_list, values, allocation)
    # Ensure envy-free
    for a in agent_list:
        for r in room_list:
            # Sample Envy example:
            # 12,0,0
            # 12,0,0
            # 3,5,4
            # For envyness uncomment below 2 lines
            # if a == r:
            #     continue
            prob += (
                price_variables[r] - price_variables[allocation[a]]
                >= values[a][r] - values[a][allocation[a]]
            )

    # Bound minimum utility
    for a in agent_list:
        prob += min_utility >= values[a][allocation[a]] - price_variables[allocation[a]]

    try:
        print("prob_envy_free")
        success(prob)
        prob.solve(PULP_CBC_CMD(msg=False))
    except:
        failure("Error occured! Couldn't solve the LP problem!")
        return

    # print(agent_list, room_list, LpStatus[prob.status])

    if LpStatus[prob.status] != OPTIMAL:
        failure("Problem solving the LP!\t" + LpStatus[prob.status])
        return None

    for a in agent_list:
        room = allocation[a]
        prices[room] = price_variables[room].value()

    return prices
