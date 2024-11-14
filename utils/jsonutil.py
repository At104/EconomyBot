import json

# -- Functions dealing with json files -- #

def read_json_file(filename: str) -> dict:

    """ Decodes all of a json file's data to a dictionary """
    try:
        with open(filename, 'r') as json_file:
            json_decoded = json.load(json_file)
            json_file.close()
    except:
        print("ERROR: Could not read from the JSON file. Check if the file exists or if the filename is correct.")
        return {}
    else:   
        return json_decoded

def write_json_file(filename: str, data: dict) -> None:

    """ Dumps json-formatted data dictionary to a json file """
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.close()
    except:
        print("ERROR: Could not write data to the JSON file. Check if the file exists or if the filename is correct.")


