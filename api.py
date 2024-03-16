from pulp import *
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from helper import *
from fair import *
from inputs import *
from constants import *

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Default API is Room
API = ROOM_API
# Hostel Feature API is only through UI for now

@app.route("/rent", methods=["GET", "POST"])
@cross_origin()
def calculate_rent():

    data = request.get_json()

    num_renters = data.get("renters", 0)
    num_rooms = data.get("rooms", 0)
    num_floors = data.get("floors", 0)
    # TODO: Add capacity
    # capacity = data.get("capacity",0)
    rent_data = data.get("rentData", [[]])

    if num_rooms == 0:
        API = HOSTEL_API
    else:
        API = ROOM_API

    # print(num_rooms, num_renters, rent_data)
    renters_list = list(range(1, num_renters + 1))
    if API == HOSTEL_API:
        floor_list = list(range(1, num_floors + 1))
    else:
        rooms_list = list(range(1, num_rooms + 1))


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
        "rents": rents,
    }

    if API == HOSTEL_API:
        response["floors"] = floor_list
    else:
        response["rooms"] = rooms_list

    return jsonify(response)


def run():
    app.run(host="127.0.0.1", port=5000)
