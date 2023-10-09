from api import *
import argparse

if __name__ == '__main__':
    #If input flag exists then take input from user
    parser = argparse.ArgumentParser()
    parser.add_argument('-input', action='store_true')
    options = parser.parse_args()
    if options.input:
        terminal_mode()
    # If file is input then work on file
    elif len( sys.argv ) > 1:
        file_name = sys.argv[1]  # Run from Local file
        maximin_utility(file_name)
    # Else run web server
    else:
        run()