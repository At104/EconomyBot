import json

# -- Functions dealing with json files -- #

def read_json_file(filename: str) -> dict:

    """ Decodes all of a json file's data to a dictionary """
    with open(filename, 'r') as json_file:
        json_decoded = json.load(json_file)
        json_file.close()

    return json_decoded

def write_json_file(filename: str, data: dict) -> None:

    """ Dumps json-formatted data dictionary to a json file """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)
        json_file.close()

