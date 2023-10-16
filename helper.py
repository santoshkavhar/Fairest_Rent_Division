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


def read_preference_csv(file_path):

    matrix = []

    # Read CSV data from the file into the list of lists
    with open(file_path, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            matrix.append([int(value) for value in row])
    return matrix


def calculate_rent(first_row):

    # Only calculate for first row
    rent = 0
    for i in first_row:
        rent += i
    return rent


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
