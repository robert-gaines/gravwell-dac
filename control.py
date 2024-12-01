from utility.configuration import Configuration
from utility.jsonify import Jsonify
import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Control():

    def __init__(self) -> None:
        self.configuration = Configuration()
        self.alerts = []
        self.queries = []
        self.searches = []

    def enumerate_alerts(self):
        for alert in os.listdir(self.configuration.alert_dir):
            if(alert.endswith('yaml')):
                self.alerts.append(os.path.join(self.configuration.alert_dir,alert))

    def enumerate_queries(self):
        for query in os.listdir(self.configuration.query_dir):
            if(query.endswith('yaml')):
                self.queries.append(os.path.join(self.configuration.query_dir,query))

    def enumerate_searches(self):
        for search in os.listdir(self.configuration.search_dir):
            if(search.endswith('yaml')):
                self.searches.append(os.path.join(self.configuration.search_dir,search))

    def upload_alerts(self):
        for alert in self.alerts:
            with open(alert, 'r') as file:
                yaml_content = file.read()
                json_content = Jsonify.jsonify_alert(yaml_content)
                response = requests.post(self.configuration.alerts_endpoint,
                                         headers=self.configuration.headers,
                                         data=json_content,
                                         verify=False)
                print(response,response.text)

    def upload_queries(self):
        for query in self.queries:
            with open(query, 'r') as file:
                yaml_content = file.read()
                json_content = Jsonify.jsonify_query(yaml_content)
                response = requests.post(self.configuration.library_endpoint,
                                         headers=self.configuration.headers,
                                         data=json_content,
                                         verify=False)
                print(response,response.text)

    def upload_searches(self):
        for search in self.searches:
            with open(search, 'r') as file:
                yaml_content = file.read()
                json_content = Jsonify.jsonify_search(yaml_content)
                response = requests.post(self.configuration.searches_endpoint,
                                         headers=self.configuration.headers,
                                         data=json_content,
                                         verify=False)
                print(response,response.text)
    
if (__name__ == '__main__'):
    control = Control()
    # control.enumerate_queries()
    # control.enumerate_searches()
    # control.upload_queries()
    # control.upload_searches()
    control.enumerate_alerts()
    control.upload_alerts()

        
    