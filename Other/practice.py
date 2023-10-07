import pulp
import random

def maximinUtility(file_name):
    with open(file_name, 'r') as file:
        n = int(file.readline())
        rent = int(file.readline())
        values = {}
        agent_set = set()
        room_set = set()

        for _ in range(n * n):
            tokens = file.readline().split()
            agent_id = tokens[0]
            agent_set.add(agent_id)
            room_id = tokens[1]
            room_set.add(room_id)
            value = int(float(tokens[2]))
            if agent_id not in values:
                values[agent_id] = {}
            values[agent_id][room_id] = value

    # First, find a welfare-maximizing allocation
    allocation = welfareMaximize(values, agent_set, room_set)

    # Now, find nonnegative price vector if possible
    prices = maximinPrices(values, agent_set, room_set, allocation, rent, True)
    if prices is None:
        #prices = maximinPrices(values, agent_set, room_set, allocation, rent, False)
        #if prices is None:
        print("failure")
        return

    for agent in agent_set:
        room = allocation[agent]
        price = prices[room]
        print(f"{agent} {room} {price}")


def welfareMaximize(values, agent_set, room_set):
    prob = pulp.LpProblem("WelfareMaximization", pulp.LpMaximize)
    variables = {}
    for a in agent_set:
        variables[a] = {}
        for r in room_set:
            variables[a][r] = pulp.LpVariable(f"x_{a}_{r}", 0, 1, pulp.LpBinary)

    # Objective is total welfare
    prob += pulp.lpSum(values[a][r] * variables[a][r] for a in agent_set for r in room_set)

    # Each agent assigned 1 room
    for a in agent_set:
        prob += pulp.lpSum(variables[a][r] for r in room_set) == 1

    # Each room assigned 1 agent
    for r in room_set:
        prob += pulp.lpSum(variables[a][r] for a in agent_set) == 1


    print(prob)
    prob.solve()

    # Get the assignment
    assignment = {}
    for a in agent_set:
        for r in room_set:
            if variables[a][r].value() == 1:
                assignment[a] = r
    return assignment


def maximinPrices(values, agent_set, room_set, assignment, rent, nonnegative_prices):
    prob = pulp.LpProblem("MaximinPrices", pulp.LpMinimize)
    price_variables = {}
    for r in room_set:
        if nonnegative_prices:
            price_variables[r] = pulp.LpVariable(f"p_{r}", 0, rent)
        else:
            price_variables[r] = pulp.LpVariable(f"p_{r}", 0)

    # Objective is maximize minimum utility (or minimize negative of minimum utility)
    min_utility = pulp.LpVariable("y", 0)
    prob += min_utility

    # Ensure prices sum to rent
    prob += pulp.lpSum(price_variables[r] for r in room_set) == rent

    # Ensure envy-free
    for i in agent_set:
        for j in agent_set:
            if i == j:
                continue
            prob += price_variables[assignment[i]] - price_variables[assignment[j]] >= values[i][assignment[j]] - values[i][assignment[i]]

    # Bound minimum utility
    #for i in agent_set:
       # prob += price_variables[assignment[i]] + min_utility >= values[i][assignment[i]]
        # Bound minimim utility
       # prob += min_utility >= values[i][assignment[i]] - (1 - price_variables[assignment[i]]) * float('inf')
    # Bound minimum utility
    for i in agent_set:
        prob += min_utility >= values[i][assignment[i]] - price_variables[assignment[i]]

    #prob.solve()


    try:
        print(prob)
        prob.solve()
    except:
        print("Error occured!")
        return
    
    if pulp.LpStatus[prob.status] == 'Optimal':
        prices = {}
        for i in agent_set:
            room = assignment[i]
            prices[room] = price_variables[room].value()
        return prices
    return None


if __name__ == "__main__":
    file_name = "input3.txt"  # Replace with your input file name
    maximinUtility(file_name)

