from helper import *
from fair import *
from csv_create import *


def terminal_mode():

    nodes = get_input_nodes()
    wt = get_input_weights(nodes)

    # wt is dictionary of dictionaries, we need to convert it
    matrix = convert_to_matrix(wt)
    file_path = generate_csv(matrix)
    maximin_utility(file_path)


def get_input_nodes():

    nodes = []

    num_nodes = int(input("Enter number of students or rooms: "))
    for i in range(num_nodes):
        # nodes will start from 1
        nodes.append(i + 1)
    return nodes


def get_input_weights(nodes):

    wt = {}

    for u in nodes:
        wt[u] = {}
        for v in nodes:
            wt[u][v] = int(
                input(
                    "Enter the preferred rent by student "
                    + str(u)
                    + " for room "
                    + str(v)
                    + " : "
                )
            )
    return wt
