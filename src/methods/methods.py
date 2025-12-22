import requests
import urllib3
import logging
import yaml
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger()

class Methods():

    def __init__(self) -> None:
        self.session = requests.Session()

    def _format_filename(self, raw_str: str) -> str:
        output = raw_str.lower()
        output = output.replace(' ', '_')
        output = output.replace('-', '_')
        output += '.yaml'
        return output

    def _check_directory_path(self, path: str) -> None:
        if os.path.exists(path):
            return True
        else:
            return False
    
    def _check_for_kit_sponsored_entity(self, labels: list) -> bool:
        if labels:
            for label in labels:
                if 'kit' in label:
                    return True
        return False
        

    def _export_data_to_file(self, output_path: str, data: dict) -> str:
        with open(output_path, 'w') as fobj:
            yaml.safe_dump(data, fobj)        

    def _categorize_entity(self, labels: list) -> str:
        ''' Using labels, categorize the entity '''
        categories = ['windows',
                      'linux',
                      'network',
                      'hypervisor',
                      'kubernetes']
        for label in labels:
            if label.lower() in categories:
                index = categories.index(label.lower())
                return categories[index]

    def _execute_get_request(self,
                             url:str,
                             headers: dict,
                             verify: bool) -> object:
        ''' Execute an HTTP GET Request & return JSON '''
        try:
            req = self.session.get(url=url,
                                   headers=headers,
                                   verify=verify)
            if req.status_code == 200:
                return req.json()
            else:
                return None
        except requests.exceptions.RequestException as e:
            logger.exception("GET Request exception raised: {0}".format(e))
            