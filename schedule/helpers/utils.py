import os
import json

def write_data_to_json(data, filename):
    if (not filename.endswith(".json")):
        filename += ".json"
    cwd = os.path.split(__file__)[0]
    filepath = cwd + ("/" if cwd else "") + '../' + filename
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def get_data_from_json(filename):
    if (not filename.endswith(".json")):
        filename += ".json"
    cwd = os.path.split(__file__)[0]
    filepath = cwd + ("/" if cwd else "") + '../' + filename
    with open(filepath) as json_file:
        data = json.load(json_file)
        return data
