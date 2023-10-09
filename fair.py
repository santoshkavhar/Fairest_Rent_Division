from pulp import *

room_list = []
agent_list = []
assignment = {}
# Default file
file_name="Other/input3.txt"


def solve_mwbm(nodes, wt):
# A Wrapper func that uses pulp to formulate and solve a MWBM

    prob = LpProblem("MWBM_Problem", LpMaximize)

    #Create the decision variables
    choices = LpVariable.dicts("edge", (nodes, nodes), 0, 1)

    max_prob = []
    for u in nodes:
        for v in nodes:
            max_prob.append(wt[u][v] * choices[u][v])

    prob += lpSum(max_prob), "Total_weight"
    
    for i in nodes:
        u_capacity_prob = []
        v_capacity_prob = []
        for j in nodes:
            # row wise constraint
            u_capacity_prob.append(choices[i][j])
            # column wise constraint
            v_capacity_prob.append(choices[j][i])
        prob += lpSum(u_capacity_prob) <= 1, ""
        prob += lpSum(v_capacity_prob) <= 1, ""

    print(prob)
    
    prob.solve()

    print("Status:", LpStatus[prob.status])
    for v in prob.variables():
        print(v.name, " = ", v.varValue )
    print("Sum of wts of selected edges= ", value(prob.objective))


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
            agent_list.append(agent_id)
            room_id = tokens[1]
            room_set.add(room_id)
            room_list.append(room_id)
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
    ass_renters_list = []
    ass_room_list = []
    ass_rents_list = []
    for agent in agent_set:
        room = allocation[agent]
        price = prices[room]
        ass_room_list.append(room)
        ass_renters_list.append(agent)
        ass_rents_list.append(price)
        print(f"{agent} {room} {price}")
    return ass_room_list, ass_renters_list, ass_rents_list


def welfareMaximize(values, agent_set, room_set):
    prob = LpProblem("WelfareMaximization", LpMaximize)
    variables = {}
    for a in agent_set:
        variables[a] = {}
        for r in room_set:
            variables[a][r] = LpVariable(f"x_{a}_{r}", 0, 1, LpBinary)

    # Objective is total welfare
    prob += lpSum(values[a][r] * variables[a][r] for a in agent_set for r in room_set)

    # Each agent assigned 1 room
    for a in agent_set:
        prob += lpSum(variables[a][r] for r in room_set) == 1

    # Each room assigned 1 agent
    for r in room_set:
        prob += lpSum(variables[a][r] for a in agent_set) == 1


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
    prob = LpProblem("MaximinPrices", LpMinimize)
    price_variables = {}
    for r in room_set:
        if nonnegative_prices:
            price_variables[r] = LpVariable(f"p_{r}", 0, rent)
        else:
            price_variables[r] = LpVariable(f"p_{r}", 0)

    # Objective is maximize minimum utility (or minimize negative of minimum utility)
    min_utility = LpVariable("y", 0)
    prob += min_utility

    # Ensure prices sum to rent
    prob += lpSum(price_variables[r] for r in room_set) == rent

    #print(agent_set, values, assignment)
    # Ensure envy-free
    for i in agent_list:
        for j in room_list:
            if i == j:
                continue
            prob += price_variables[j] - price_variables[assignment[i]] >= values[i][j] - values[i][assignment[i]]

    # Bound minimum utility
    for i in agent_set:
        prob += min_utility >= values[i][assignment[i]] - price_variables[assignment[i]]

    try:
        print(prob)
        prob.solve()
    except:
        print("Error occured!")
        return
    
    if LpStatus[prob.status] == 'Optimal':
        prices = {}
        for i in agent_set:
            room = assignment[i]
            prices[room] = price_variables[room].value()
        return prices
    return None
