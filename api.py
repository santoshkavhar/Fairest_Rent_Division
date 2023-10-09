from pulp import *
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from helper import *
from fair import *

room_list = []
agent_list = []
assignment = {}
# Default file
file_name="Other/input3.txt"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'  

@app.route('/api', methods=['GET','POST'])
@cross_origin()
def calculate_rent():
    data = request.get_json()
    # TODO: Use below variables
    num_renters = data.get('renters', 0)
    num_rooms = data.get('rooms', 0)
    rent_data = data.get('rentData', [[]])
    print(num_rooms, num_renters, rent_data)
    renters_list = list(range(1, num_renters+1))
    rooms_list = list(range(1, num_rooms+1))
    wt = convert_rent_data(rent_data)
    file_name = createFile(renters_list, wt)
    rooms_list, renters_list, rents = maximinUtility(file_name)
    # TODO: Get assignment data
    response = {
        'file_name': file_name,
        'renters': renters_list,
        'rooms': rooms_list,
        'rents': rents
    }

    return jsonify(response)

def run():
    # TODO: If input flag exists then take input from user

    if len( sys.argv ) > 1:
        file_name = sys.argv[1]  # Run from Local file
        maximinUtility(file_name)
    else:
        # Run web server
        app.run(host='127.0.0.1', port=5000)