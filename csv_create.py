import numpy as np
import csv
import random
import string
import os
import time
from constants import *
from helper import *


def create_csv_files(num_files, folder_name, API):

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for i in range(num_files):
        generate_csv(folder_name, API)


def correct_matrix(matrix, rent):

    for i, row in enumerate(matrix):
        sum = 0
        # print(i, row)
        for _, ele in enumerate(row):
            # print(ele)
            sum += ele

        if sum < rent:
            # Choose a random index to add the difference of rent
            random_index = random.randint(0, len(row) - 1)
            # print(random_index)
            matrix[i][random_index] = matrix[i][random_index] + rent - sum

    return matrix


def generate_csv(matrix_or_folder, API):

    if matrix_or_folder is None:
        return generate_random_csv(MIN_RENT, MAX_RENT, MIN_ROWS, MAX_ROWS, API)

    # Check if parameter is a string i.e a folder name
    elif type(matrix_or_folder) == str:
        folder_name = matrix_or_folder
        return generate_random_csv(MIN_RENT, MAX_RENT, MIN_ROWS, MAX_ROWS, folder_name, API)

    else:
        matrix = matrix_or_folder
        return generate_csv_from_matrix(matrix, None)


def generate_random_csv(min_rent, max_rent, min_rows, max_rows, folder_name, API):

    # Change the value of n as needed
    # n = 5 For a 5x5 matrix
    # Generate n x n matrix with random integers

    # Random Rent range -> [10,1000]
    rent = random.randint(min_rent, max_rent)
    # Random square matrix row length range -> [3,10]
    n = random.randint(min_rows, max_rows)

    matrix = np.random.randint(0, rent + 1, size=(n, n))

    # Ensure each row sums up to rent
    matrix = (matrix / matrix.sum(axis=1)[:, np.newaxis]) * rent

    # Convert the matrix to integer values as above gives floats
    matrix = matrix.astype(int)

    # Correct the matrix as convertion has some loss to rent
    matrix = correct_matrix(matrix, rent)

    # print(matrix)
    return generate_csv_from_matrix(matrix, folder_name)


def generate_csv_from_matrix(matrix, folder_name):

    # Get default folder
    f_n = CSV_Input

    # Check if data is to be created inside given folder
    if folder_name is not None:
        f_n = folder_name

    # Write the matrix to a CSV file
    file_name = (
        "in_"
        + str(time.time())
        + "_"
        + "".join(random.choices(string.ascii_lowercase, k=6))
        + ".csv"
    )
    file_path = os.path.join(f_n, file_name)

    # Create directory if not already exist
    os.makedirs(f_n, exist_ok=True)

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in matrix:
            writer.writerow(row)
    return file_path


def generate_csv_for_hostel(rent, capacity, floor_names, renters_floors, folder_name):
    # Get default folder
    f_n = CSV_Input_Hostel

    # Check if data is to be created inside given folder
    if folder_name is not None:
        f_n = folder_name

    # Write the matrix to a CSV file
    file_name = (
        "in_"
        + str(time.time())
        + "_"
        + "".join(random.choices(string.ascii_lowercase, k=6))
        + ".csv"
    )
    file_path = os.path.join(f_n, file_name)

    # Create directory if not already exist
    os.makedirs(f_n, exist_ok=True)

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Write rent
        # help("Writing")
        writer.writerow([rent])
        writer.writerow(capacity)
        writer.writerow(floor_names)
        for row in renters_floors:
            writer.writerow(row)
    return file_path
