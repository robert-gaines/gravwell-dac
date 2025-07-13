from src.utility.searches import Searches
from src.utility.queries import Queries
from src.utility.parsing import Parsers
import requests
import urllib3
import logging
import yaml
import sys
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

class Control():

    def __init__(self, token: str) -> None:
        self.fqdn = ''
        self.token = token
        self.parser = Parsers()
        self.alerts = []
        self.queries = []
        self.searches = []
        self.filename = "src/configuration/configuration.yaml"
        self.parse_config()
        self.alert_dir = 'src/alerts'
        self.query_dir = 'src/queries'
        self.search_dir = 'src/scheduled-searches'
        self.alerts_endpoint = f"https://{self.fqdn}/api/alerts"
        self.library_endpoint = f"https://{self.fqdn}/api/library"
        self.searches_endpoint = f"https://{self.fqdn}/api/scheduledsearches"
        self.headers = {
            "Gravwell-Token": self.token, 
            "Content-Type": "application/json"
        }
        self.query_session = Queries(self.fqdn, self.headers)
        self.search_session = Searches(self.fqdn, self.headers)

    def parse_config(self) -> None:
        try:
            if os.path.exists(self.filename):
                logging.info("Located configuration file")
                with open(self.filename, 'r') as file_handle:
                    self.configuration = yaml.safe_load(file_handle)
                    self.configuration = self.configuration['configuration']
                    self.fqdn = self.configuration['fqdn']
        except Exception as e:
            logging.exception("Exception raised: {0}".format(e))
            sys.exit()

    def enumerate_alerts(self):
        for alert in os.listdir(self.alert_dir):
            if(alert.endswith('yaml')):
                self.alerts.append(os.path.join(self.alert_dir,alert))
        logging.info(self.alerts)

    def enumerate_queries(self):
        for query in os.listdir(self.query_dir):
            if(query.endswith('yaml')):
                self.queries.append(os.path.join(self.query_dir,query))

    def enumerate_searches(self):
        for search in os.listdir(self.search_dir):
            if(search.endswith('yaml')):
                self.searches.append(os.path.join(self.search_dir,search))

    def upload_alerts(self):
        for alert in self.alerts:
            with open(alert, 'r') as file:
                yaml_content = file.read()
                json_content = self.parser.jsonify_alert(yaml_content)
                response = requests.post(self.alerts_endpoint,
                                         headers=self.headers,
                                         data=json_content,
                                         verify=False)
                print(response,response.text)

    def upload_queries(self):
        for query in self.queries:
            with open(query, 'r') as file:
                yaml_content = file.read()
                json_content = self.parser.jsonify_query(yaml_content)
                response = requests.post(self.library_endpoint,
                                         headers=self.headers,
                                         data=json_content,
                                         verify=False)
                print(response,response.text)

    def upload_searches(self):
        for search in self.searches:
            with open(search, 'r') as file:
                yaml_content = file.read()
                json_content = self.parser.jsonify_search(yaml_content)
                response = requests.post(self.searches_endpoint,
                                         headers=self.headers,
                                         data=json_content,
                                         verify=False)
                print(response,response.text)
    
if (__name__ == '__main__'):
    token = ""
    control = Control(token)
    # control.enumerate_queries()
    # control.enumerate_searches()
    # control.upload_queries()
    # control.upload_searches()
    # control.enumerate_alerts()
    # control.query_session.get_queries()
    # control.search_session.get_searches()
    # control.search_session.export_searches()
    control.search_session.stage_search_data_from_files()
    # control.upload_alerts()

        
    