# Fairest_Rent_Division
Based on paper of "Which is the Fairest (Rent Division) of them all"

# Setup
## Virtual environment setup
### Install Virtual Environment
pip3 install virtualenv
### Create Virtual Environment
virtualenv venv
### Activate Virtual Environment
source venv/bin/activate

## Install Requirements
pip3 install -r requirements.txt

# Run
## Help to Run application
python3 app.py --help 

## Web Server mode
python3 app.py

## Terminal mode
python3 app.py -terminal

## Input File mode
python3 app.py -file <file_path>

## Create CSV files for rent data
python3 app.py -create <num_of_files_to_be_created> <folder_name>

## Test CSV files for rent data
python3 app.py -test <folder_name>

## For hostel mode use hostel flag
python3 app.py -terminal -hostel

# NOTE:
Please start folder_name for creation of CSV files to be something like Test*, where * can be any string.

# For Help with arguments
python3 app.py -h

