from pulp import *


def get_input_nodes():
    nodes = []
    num_nodes = int(input("Enter number of students or rooms: "))
    for i in range(num_nodes):
        # nodes will start from 1
        nodes.append(i+1)
    return(nodes)
    

def get_input_weights(nodes):
    wt = {}
    for u in nodes:
        wt[u] = {}
        for v in nodes:
            wt[u][v] = int(input("Enter the rent preferance by student "+ str(u)+ " for room "+ str(v) +" : "))
    return(wt)

    

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


nodes = get_input_nodes()
wt= get_input_weights(nodes)
solve_mwbm(nodes, wt)
