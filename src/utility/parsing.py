import yaml
import json
import re

class Parsers():

    def __init__(self) -> None:
        return

    def jsonify_query(self, yaml_content):
        data = yaml.safe_load(yaml_content)
        json_payload = data[0]['query']
        json_output = json.dumps(json_payload, indent=2)
        return json_output
    
    def jsonify_search(self, yaml_content):
        data = yaml.safe_load(yaml_content)
        json_payload = data['search']
        json_output = json.dumps(json_payload, indent=2)
        return json_output
    
    def jsonify_alert(self, yaml_content):
        data = yaml.safe_load(yaml_content)
        json_payload = data[0]['alert']
        json_output = json.dumps(json_payload, indent=2)
        return json_output
    
    def write_yaml_file(self, filename: str, data: yaml) -> None:
        with open(filename, 'w') as fileobj:
            yaml.safe_dump(data, fileobj, default_flow_style=False)

    def remove_characters(self, input: str) -> str:
        res = re.sub(r'[^a-zA-Z0-9]', '_', input)
        return res
