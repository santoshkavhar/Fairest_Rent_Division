import os
from helper import *
from fair import *

capacity = [1]*100

def test_csv_files(folder_name, API):

    # Check if the folder exists
    if folder_name is None or not os.path.exists(folder_name):
        failure(f"Please provide correct folder name. Given Folder does not exist.")
        return

    # List all files in the folder
    files = os.listdir(folder_name)
    for file in files:
        file_path = os.path.join(folder_name, file)
        help(f"Testing file: " + file_path)
        maximin_utility(file_path, capacity, API)
