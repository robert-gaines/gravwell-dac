import yaml
import json

class Jsonify():

    def __init__(self) -> None:
        return

    def jsonify_query(yaml_content):
        data = yaml.safe_load(yaml_content)
        json_payload = data[0]['query']
        json_output = json.dumps(json_payload, indent=2)
        return json_output
    
    def jsonify_search(yaml_content):
        data = yaml.safe_load(yaml_content)
        json_payload = data[0]['search']
        json_output = json.dumps(json_payload, indent=2)
        return json_output
    
    def jsonify_alert(yaml_content):
        data = yaml.safe_load(yaml_content)
        json_payload = data[0]['alert']
        json_output = json.dumps(json_payload, indent=2)
        return json_output