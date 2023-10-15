import os
from helper import *
from create_input import *


def create_csv_files(num_files, folder_name):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for i in range(num_files):        
        generate_csv(folder_name)

def test_csv_files(folder_name):
    # Check if the folder exists
    if not os.path.exists(folder_name):
        failure(f'Folder "{folder_name}" does not exist.')
        return

    # List all files in the folder
    files = os.listdir(folder_name)
    for file in files:
        help(f'Testing file: {os.path.join(folder_name, file)}')



