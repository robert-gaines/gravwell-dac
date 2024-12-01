from configuration import Configuration
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

c = Configuration()

def get_alerts():
    url = f"https://{c.siem}/api/alerts"
    req = requests.get(url, headers=c.headers, verify=False)
    print(req.json())
    print()
    for entry in req.json():
        for value in entry.keys():
            print(f"{value}: {entry[value]}")

get_alerts()