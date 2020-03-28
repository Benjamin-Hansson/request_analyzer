import json
import os

data_dictionary = "collected_data/list"
ending = ".json"


# Returns dictionary from data file
def read_data_file(number):
    if os.path.exists(data_dictionary+str(number)+ending):
        with open(data_dictionary + str(number) + ending, "r") as file:
            data = json.loads(file.read())
            return data if data else {}
    write_data_file({}, number)
    return {}


# Writes dictionary to data file
def write_data_file(dict, number):
    with open(data_dictionary + str(number) + ending, "w+") as file:
        file.write(json.dumps(dict, indent=6))
