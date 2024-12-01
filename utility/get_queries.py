from configuration import Configuration
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

c = Configuration()

def get_queries():
    url = f"https://{c.siem}/api/library"
    req = requests.get(url, headers=c.headers, verify=False)
    for entry in req.json():
        print(entry)

get_queries()