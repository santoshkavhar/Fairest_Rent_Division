from pulp import *


def solve_mwbm(nodes, wt):
    # A Wrapper func that uses pulp to formulate and solve a MWBM

    prob = LpProblem("MWBM_Problem", LpMaximize)

    # Create the decision variables
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
        print(v.name, " = ", v.varValue)
    print("Sum of wts of selected edges= ", value(prob.objective))


def create_file(nodes, wt):
    # 16 random letters input file to be created
    res = (
        "Inputs/in_"
        + str(time.time())
        + "_"
        + "".join(random.choices(string.ascii_lowercase, k=6))
        + ".txt"
    )
    f = open(res, "w")
    # We can get number of nodes as the first line
    f.write(str(len(nodes)) + "\n")
    rent = 0
    print(wt)
    # Second line will be the sum of rent of all rooms for any agent, consider first agent
    for i in nodes:
        rent += wt[1][i]
    f.write(str(rent) + "\n")
    for i in nodes:
        for j in nodes:
            f.write(str(i) + " " + str(j) + " " + str(wt[i][j]) + "\n")
    f.close()
    return res


def check_for_folder_name():
    if args.folder_name == "":
        failure("Folder Name has to be passed!")
        exit(1)
