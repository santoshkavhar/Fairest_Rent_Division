from sys import argv
from api import *
from create_csvs import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create, test files, or run specified functions based on flags.')
    parser.add_argument('-create', type=int, help='Create CSV files. Provide the number of files to create.', metavar='NUM_FILES')
    parser.add_argument('-test', action='store_true', help='Test CSV files in the folder.')
    parser.add_argument('-terminal', action='store_true', help='Run terminal mode of program.')
    parser.add_argument('-file', type=str, help='Take input from a CSV file with the specified file path.', metavar='FILE_PATH')
    # Make 'folder_name' compulsory only for -create and -test flags
    parser.add_argument('folder_name', type=str, help='Folder name.')
    
    args = parser.parse_args()

    # Highest priority
    if args.terminal:
        terminal_mode()
    elif args.file:
        maximin_utility(args.file)
    elif args.create:
        create_csv_files(args.create, args.folder_name)
    elif args.test:
        test_csv_files(args.folder_name)
    else:
        # Run web server by default
        run()