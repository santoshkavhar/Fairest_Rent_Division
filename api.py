from pulp import *
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from helper import *
from fair import *
from inputs import *

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
    file_name = create_file(renters_list, wt)
    
    ret_value = maximin_utility(file_name)
    if ret_value is None:
        return jsonify({'file_name': file_name, 'error':'Validation failed!'})
    rooms_list, renters_list, rents = ret_value
    response = {
        'file_name': file_name,
        'renters': renters_list,
        'rooms': rooms_list,
        'rents': rents
    }

    return jsonify(response)

def run():
    app.run(host='127.0.0.1', port=5000)