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
    # capacity is in string form e.g. capacity="2,3,4"
    capacity_string = data.get("capacity","")
    rent_data = data.get("rentData", [[]])
    rent = data.get("rent", 0)

    success(type(capacity_string))
    success(rent_data)

    if num_rooms == 0:
        API = HOSTEL_API
        capacity = generate_capacity_list(capacity_string, num_floors)
        # Normalized rent data
        rent_data = normalized_rent_data(rent_data, capacity, rent)
    else:
        API = ROOM_API
        # Default capacity = 1,1,1...
        capacity = [1]*num_rooms

    # print(num_rooms, num_renters, rent_data)
    renters_list = list(range(1, num_renters + 1))
    # if API == HOSTEL_API:
    #     floors_list = list(range(1, num_floors + 1))
    # else:
    #     rooms_list = list(range(1, num_rooms + 1))


    # Rent data is already in matrix format
    file_path = generate_csv(rent_data)
    ret_value = maximin_utility(file_path, capacity)

    if ret_value is None:
        err_response = {
            "file_path": file_path,
            "error": "Validation failed or No solution found!"
        }
        return jsonify(err_response)

    if API == HOSTEL_API:
        floors_list, renters_list, rents = ret_value
    else:
        rooms_list, renters_list, rents = ret_value

    rents = normalize_final_rent(rents, rent)

    response = {
        "file_path": file_path,
        "renters": renters_list,
        "rents": rents,
        "normalized_rent_data": rent_data,
    }

    if API == HOSTEL_API:
        response["floors"] = floors_list
    else:
        response["rooms"] = rooms_list

    return jsonify(response)


def run():
    app.run(host="127.0.0.1", port=5000)
