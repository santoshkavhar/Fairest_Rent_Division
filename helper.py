import random
import string
import time

def convert_rent_data(rent_data):
    wt = {}
    for i, sublist in enumerate(rent_data, start=1):
        wt[i] = {}
        for j, value in enumerate(sublist, start=1):
            wt[i][j] = value
    return wt

def create_file(nodes, wt):
    # 16 random letters input file to be created
    res = "Inputs/input_" + str(int(time.time()))+ ''.join(random.choices(string.ascii_lowercase, k=6)) + ".txt"
    f = open(res, "w")
    # We can get number of nodes as the first line
    f.write(str(len(nodes))+"\n")
    rent = 0
    print(wt)
    # Second line will be the sum of rent of all rooms for any agent, consider first agent
    for i in nodes:
        rent += wt[1][i]
    f.write(str(rent) + "\n")
    for i in nodes:
        for j in nodes:
            f.write(str(i) + " " + str(j) + " " + str(wt[i][j])+"\n")
    f.close()
    return res