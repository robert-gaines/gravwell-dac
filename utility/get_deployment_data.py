from configuration import Configuration
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

c = Configuration()

def get_deployment_data():
    url = f"https://{c.siem}/api/deployment"
    req = requests.get(url, headers=c.headers, verify=False)
    print(req.json())

get_deployment_data()