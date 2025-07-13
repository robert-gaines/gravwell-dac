from src.utility.parsing import Parsers
import requests
import urllib3
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)

class Queries():

    def __init__(self, fqdn: str, headers: object) -> None:
        self.fqdn = fqdn
        self.headers = headers
        self.parsers = Parsers()
        self.queries = []

    def get_queries(self) -> None:
        logging.info("Retrieving all non-kit queries from the library")
        url = f"https://{self.fqdn}/api/library"
        req = requests.get(url, headers=self.headers, verify=False)
        if req.status_code == 200:
            for entry in req.json():
                self.queries.append(entry)
        else:
            logging.error("Failed to retrieve queries from the SIEM")
        