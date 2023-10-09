from sys import argv
from api import *

if __name__ == '__main__':
    #If input flag exists then take input from user
    if '-input' in sys.argv:
        terminal_mode()
    # If file is input then work on file
    elif len( sys.argv ) > 1:
        file_name = sys.argv[1]  # Run from Local file
        maximin_utility(file_name)
    # Else run web server
    else:
        run()