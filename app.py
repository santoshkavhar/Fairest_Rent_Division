from api import *
from csv_create import *
from csv_test import *
import argparse

capacity = [1]*100

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create, test files, or run specified functions based on flags."
    )
    parser.add_argument(
        "-create",
        type=int,
        help="Create CSV files. Provide the number of files to create in a folder. Thus it needs folder name.",
        metavar="NUM_FILES",
    )
    parser.add_argument(
        "-test",
        action="store_true",
        help="Test CSV files in the folder. Thus it needs folder name.",
    )
    parser.add_argument(
        "-terminal",
        action="store_true", 
        help="Run terminal mode of program."
    )
    parser.add_argument(
        "-file",
        type=str,
        help="Take input from a CSV file with the specified file path.",
        metavar="FILE_PATH",
    )
    parser.add_argument(
        "-hostel",
        action="store_true", 
        help="Run hostel mode of program."
    )

    # Make 'folder_name' compulsory only for -create and -test flags
    parser.add_argument("folder_name", type=str, nargs="?", help="Folder name.")

    args = parser.parse_args()
    if args.hostel:
        API = HOSTEL_API
    # Highest priority
    if args.terminal:
        terminal_mode(API)
    elif args.file:
        maximin_utility(args.file, API)
    elif args.create:
        create_csv_files(args.create, args.folder_name, API)
    elif args.test:
        test_csv_files(args.folder_name, API)
    else:
        # Run web server by default
        run()
