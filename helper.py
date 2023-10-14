import random
import string
import time
import csv
from constants import *

# To dictionary format
def convert_rent_data(rent_data):
    wt = []
    for i, sublist in enumerate(rent_data, start=1):
        wt[i]
        for j, value in enumerate(sublist, start=1):
            wt[i][j] = value
    return wt

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
    with open(file_path, 'r') as csvfile:
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

def set_failure():
    print(bcolors.FAIL)

def set_normal():
    print(bcolors.ENDC)