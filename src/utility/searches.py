from src.utility.parsing import Parsers
import requests
import urllib3
import logging
import yaml
import json
import os
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

class Searches():

    def __init__(self, fqdn:str, headers: object) -> None:
        self.fqdn = fqdn
        self.parser = Parsers()
        self.headers = headers
        self.scheduled_searches = []
        self.url = f"https://{self.fqdn}/api/scheduledsearches"
    
    def get_searches(self):
        req = requests.get(self.url, headers=self.headers, verify=False)
        if req.status_code == 200:
            logging.info("Succesfully retrieved scheduled searches")
            for entry in req.json():
                self.scheduled_searches.append(entry)
        else:
            logging.error("Failed to retrieve scheduled searches")
        logging.info("Retrieved {0} scheduled searches".format(len(self.scheduled_searches)))

    def export_searches(self) -> None:
        current_directory = os.getcwd()
        req = requests.get(self.url, headers=self.headers, verify=False)
        if req.status_code == 200:
            os.chdir('src/searches')
            for entry in req.json():
                filename = entry['Name']
                filename = self.parser.remove_characters(filename)
                filename = filename + '.yaml'
                filename = filename.lower()
                entry = {"search":entry}
                self.parser.write_yaml_file(filename, entry)
                logging.info("Exporting scheduled search to: {0}".format(filename))
        os.chdir(current_directory)

    def stage_search_data_from_files(self) -> None:
        current_directory = os.getcwd()
        os.chdir('src/searches')
        for file in  os.listdir():
            with open(file, 'r') as fileobj:
                payload = self.parser.jsonify_search(fileobj) 
                logging.info(payload)