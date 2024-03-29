import csv
from constants import *

# Convert ao list of lists from a dictionary of dictionaries format
def convert_to_matrix(rent_data):

    matrix = []

    for _, inner_dict in rent_data.items():
        row = []

        row.extend(inner_dict.values())  # Add the values from the inner dictionary
        matrix.append(row)
    return matrix


def check_matrix(matrix):
    for row in matrix:
        sum = 0
        # print(i, row)
        for ele in row:
            # print(j, ele)
            sum += ele
        print(sum)


def read_preference_csv(file_path, API):

    matrix = []

    # Read CSV data from the file into the list of lists
    with open(file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        if API == HOSTEL_API:
        # Skip first 3 rows of rent, capacity and floor names
            rent = next(csv_reader)
            capacity_string = next(csv_reader)
            # warning(capacity_string)
            capacity = [eval(i) for i in capacity_string]
            next(csv_reader)
        for row in csv_reader:
            matrix.append([float(value) for value in row])

    if API == HOSTEL_API:
        # Normalize only if it is HOSTEL_API
        rent_data = normalized_rent_data(matrix, capacity, int(rent[0]))
        return rent_data, int(rent[0])
    return matrix, None


def calculate_rent(first_row):

    # Only calculate for first row
    rent = 0
    for i in first_row:
        rent += i
    return rent

def generate_capacity_list(capacity_string, num_floors):
    # Split the string by comma, converting them to integers
    capacity_list = []
    capacity_string = capacity_string.split(',')
    capacity_list.extend(capacity_string)
    capacity_list = [eval(i) for i in capacity_list]
    if len(capacity_list) < num_floors:
    # Add dummy values
        capacity_list.extend([1]*num_floors)
    print(capacity_list)
    # Return a list of these capacity integers
    return capacity_list

def normalized_rent_data(rent_data, capacity, rent):
    normalized_rent_data = rent_data.copy()  # Making a copy to avoid modifying original data
    for i in range(len(rent_data)):
        total_capacity = sum(rent_data[i][j] * capacity[j] for j in range(len(rent_data[i])))
        print("total capacity")
        warning(total_capacity)

        normalize_x = rent / total_capacity
        print("normalize_x")
        warning(normalize_x)

        for j in range(len(rent_data[i])):
            # Formula includes capacity as well
            normalized_rent_data[i][j] = rent_data[i][j] * capacity[j] * normalize_x
    print("Norm values: ", normalized_rent_data)
    return normalized_rent_data

def normalize_final_rent(rents, rent):
    warning("rents")
    warning(rents)
    warning("rent")
    warning(rent)
    normalized_rent_data = rents.copy() # Making a copy
    total_sum = sum(rents)
    for i in range(len(rents)):
        # print("Normal", i)
        normalized_rent_data[i] = rents[i] * rent / total_sum
    return normalized_rent_data


def convert_list_of_list_of_strings_to_int(list_of_list_of_strings):
  result = []
  for sublist in list_of_list_of_strings:
    inner_result = []
    for string in sublist:
      inner_result.append(int(string))
    result.append(inner_result)
  return result

def failure(input):
    print(bcolors.FAIL, input, bcolors.ENDC)


def warning(input):
    print(bcolors.WARNING, input, bcolors.ENDC)


def success(input):
    print(bcolors.SUCCESS, input, bcolors.ENDC)


def help(input):
    print(bcolors.OKCYAN, input, bcolors.ENDC)

def set_bold():
    print(bcolors.BOLD) 

def set_failure():
    print(bcolors.FAIL)


def set_normal():
    print(bcolors.ENDC)
