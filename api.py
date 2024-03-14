from pulp import *
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from helper import *
from fair import *
from inputs import *

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/api", methods=["GET", "POST"])
@cross_origin()
def calculate_rent():

    data = request.get_json()

    num_renters = data.get("renters", 0)
    num_rooms = data.get("rooms", 0)
    rent_data = data.get("rentData", [[]])

    # print(num_rooms, num_renters, rent_data)
    renters_list = list(range(1, num_renters + 1))
    rooms_list = list(range(1, num_rooms + 1))

    # Rent data is already in matrix format
    file_path = generate_csv(rent_data)
    ret_value = maximin_utility(file_path)

    if ret_value is None:
        err_response = {
            "file_path": file_path,
            "error": "Validation failed!"
        }
        return jsonify(err_response)

    rooms_list, renters_list, rents = ret_value

    response = {
        "file_path": file_path,
        "renters": renters_list,
        "rooms": rooms_list,
        "rents": rents,
    }

    return jsonify(response)


@app.route("/hostel_api", methods=["GET", "POST"])
@cross_origin()
def calculate_hostel_rent():

    data = request.get_json()

    num_renters = data.get("renters", 0)
    num_floors = data.get("floors", 0)
    # TODO: Add capacity
    # capacity = data.get("capacity",0)
    rent_data = data.get("rentData", [[]])

    # print(num_floors, num_renters, rent_data)
    renters_list = list(range(1, num_renters + 1))
    rooms_list = list(range(1, num_floors + 1))

    print(renters_list,rooms_list)
    # Rent data is already in matrix format
    file_path = generate_csv(rent_data)

    ret_value = maximin_utility(file_path)

    if ret_value is None:
        err_response = {
            "file_path": file_path,
            "error": "Validation failed or No solution found!"
        }
        return jsonify(err_response)

    rooms_list, renters_list, rents = ret_value

    response = {
        "file_path": file_path,
        "renters": renters_list,
        "floors": rooms_list,
        "rents": rents,
    }

    return jsonify(response)


def run():
    app.run(host="127.0.0.1", port=5000)
