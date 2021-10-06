import json


def save_json(data):
    json_data = json.loads(data)
    with open('request.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)