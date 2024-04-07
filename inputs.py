from helper import *
from fair import *
from csv_create import *

# capacity = [1] * 100

def terminal_mode(API):

    if API == ROOM_API:
        matrix = get_matrix_for_room()
        file_path = generate_csv(matrix, API)
    else:
        rent, capacity, floor_names, renters_floors = get_inputs_for_hostel()
        file_path = generate_csv_for_hostel(rent, capacity, floor_names, renters_floors, CSV_Input_Hostel)
    # For hostel_api the csv is of different format

    maximin_utility(file_path, API, False)


def get_matrix_for_room():
    nodes = get_input_nodes()
    wt = get_input_weights(nodes)

    # wt is dictionary of dictionaries, we need to convert it
    return convert_to_matrix(wt)


def get_inputs_for_hostel():
    capacity = []
    floor_names = []

    renters_floors = []

    # Get total rent
    rent =  int(input("Enter total rent: "))

    # Get no. of floors
    num_floors = int(input("Enter number of floors: "))

    # Get capacity
    for i in range(num_floors):
        cap_i = int(input("Enter capacity of floor "+ str(i+1) + ": "))
        capacity.append(cap_i)

    # Get floor names
    for i in range(num_floors):
        floor_name = input("Enter name of floor no. "+ str(i+1)+ ": ")
        floor_names.append(floor_name)

    # Get no. of renters
    num_renters = int(input("Enter number of renters: "))

    # Loop over renters, floors
    for i in range(num_renters):
        renter_floors_i = []
        for j in range(num_floors):
            renter_floors_i.append(
                int(
                input(
                "Enter the preferred rent by renter "
                + str(i+1)
                + " for floor "
                + str(j+1)
                + " : "
            )))
        renters_floors.append(renter_floors_i)

    return rent, capacity, floor_names, renters_floors



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
