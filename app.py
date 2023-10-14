from sys import argv
from api import *

if __name__ == '__main__':
    #If input flag exists then take input from user
    if '-input' in sys.argv:
        terminal_mode()
    # If file is input then work on file
    elif len( sys.argv ) > 1:
        file_path = sys.argv[1]  # Run from Local file
        maximin_utility(file_path)
    # TODO: Create and run random number of files for certain parameters in command line
    # Else run web server
    else:
        run()