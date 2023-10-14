import numpy as np
import csv
import random
import string
import time

def correct_matrix(matrix, rent):
    for i, row in enumerate(matrix):
        sum = 0
        # print(i, row)
        for _, ele in enumerate(row):
            # print(j, ele)
            sum += ele
        if sum < rent:
            # Choose a random index to add the difference of rent
            random_index = random.randint(0, len(row)-1)
            # print(random_index)
            matrix[i][random_index] = matrix[i][random_index] + rent-sum
    return matrix
            

def generate_csv(matrix):
    if matrix is None:
        # Rent range [10,1000]
        min_rent = 10
        max_rent = 1000
        min_rows = 3
        max_rows = 10
        # row/col length range -> [3,10]
        return generate_random_csv(min_rent, max_rent, min_rows, max_rows)
    
    else:
        return generate_csv_from_matrix(matrix)

def generate_random_csv(min_rent, max_rent, min_rows, max_rows):

    # Change the value of n as needed
    # n = 5 For a 5x5 matrix
    # Generate n x n matrix with random integers

    # Random Rent range -> [10,1000]
    rent = random.randint(min_rent, max_rent)
    # Random square matrix row length range -> [3,10]
    n = random.randint(min_rows, max_rows)

    matrix = np.random.randint(0, rent+1, size=(n, n))
    
    # Ensure each row sums up to rent
    matrix = (matrix / matrix.sum(axis=1)[:, np.newaxis]) * rent
    
    # Convert the matrix to integer values as above gives floats
    matrix = matrix.astype(int)

    # Correct the matrix as convertion has some loss to rent
    matrix = correct_matrix(matrix, rent)

    # print(matrix)
    return generate_csv_from_matrix(matrix)


def generate_csv_from_matrix(matrix):

    # Write the matrix to a CSV file
    file_path = 'CSV_Input/in_' + str(time.time())+ "_" + ''.join(random.choices(string.ascii_lowercase, k=6)) + '.csv'
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in matrix:
            writer.writerow(row)
    return file_path
