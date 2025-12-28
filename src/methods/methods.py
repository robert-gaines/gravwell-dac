import requests
import urllib3
import logging
import uuid
import yaml
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger()

class Methods():

    def __init__(self) -> None:
        self.session = requests.Session()

    def _generate_uuid(self) -> None:
        return str(uuid.uuid4())

    def _format_filename(self, raw_str: str) -> str:
        output = raw_str.lower()
        output = output.replace(' ', '_')
        output = output.replace('-', '_')
        output = output.replace(':', '_')
        output += '.yaml'
        return output

    def _check_directory_path(self, path: str) -> None:
        ''' Checks for the validity of a given path '''
        if os.path.exists(path):
            return True
        else:
            return False
    
    def _check_for_kit_sponsored_entity(self, labels: list) -> bool:
        ''' 
        Check for kit affiliated objects.
        Given that kit objects may have other dependencies, 
        we want to avoid modifying these objects 
        '''
        if labels:
            for label in labels:
                if 'kit' in label:
                    return True
        return False

    def _purge_directory(self, path: str) -> None:
        for entity in os.listdir(path):
            for object in os.listdir(f"{path}/{entity}"):
                if object.endswith('.yaml'):
                    try:
                        os.remove(f"{path}/{entity}/{object}")
                    except Exception as e:
                        logging.exception("Exception raised: {0}".format(e))

    def _check_for_deltas(self, remote_obj: dict, local_obj: dict) -> bool:
        if local_obj != remote_obj:
            return True
        return False

    def _export_data_to_file(self, output_path: str, data: dict) -> str:
        ''' Export dictionary formatted data to a yaml file '''
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

    def _delete_variable_search_fields(self, scheduled_search_object: dict) -> dict:
        del scheduled_search_object['LastRun']
        del scheduled_search_object['LastRunDuration']
        del scheduled_search_object['LastSearchIDs']
        return scheduled_search_object

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

    def _execute_put_request(self,
                             url:str,
                             headers: dict,
                             payload: dict,
                             verify: bool) -> int:
        ''' Execute an HTTP PUT Request '''
        try:
            req = self.session.put(url=url,
                                   headers=headers,
                                   json=payload,
                                   verify=verify)
            return req.status_code
        except requests.exceptions.RequestException as e:
            logger.exception("PUT Request exception raised: {0}".format(e))

    def _execute_post_request(self,
                             url:str,
                             headers: dict,
                             payload: dict,
                             verify: bool) -> int:
        ''' Execute an HTTP POST Request '''
        try:
            req = self.session.post(url=url,
                                    headers=headers,
                                    json=payload,
                                    verify=verify)
            return req.status_code
        except requests.exceptions.RequestException as e:
            logger.exception("POST Request exception raised: {0}".format(e))
            
    def _execute_delete_request(self,
                             url:str,
                             headers: dict,
                             verify: bool) -> object:
        ''' Execute an HTTP DELETE Request '''
        try:
            req = self.session.delete(url=url,
                                      headers=headers,
                                      verify=verify)
            return req.status_code
        except requests.exceptions.RequestException as e:
            logger.exception("DELETE Request exception raised: {0}".format(e))