from configuration import Configuration
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

c = Configuration()

def get_searches():
    url = f"https://{c.siem}/api/scheduledsearches"
    req = requests.get(url, headers=c.headers, verify=False)
    for entry in req.json():
        for value in entry.keys():
            print(f"{value}: {entry[value]}")

get_searches()