from src.methods.methods import Methods
import logging
import yaml
import os

logger = logging.getLogger()

class Searches(Methods):

    def __init__(self, headers: dict, url: str) -> None:
        self.headers = headers
        self.url = url
        super().__init__()
    
    def _get_library_searches(self) -> None:
        ''' Retrieve current Library Searches '''
        url = f"{self.url}/library"
        library_search_path= "src/data/library_searches/"
        super()._purge_directory(library_search_path)
        searches = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(library_search_path):
            for search in searches:
                if not super()._check_for_kit_sponsored_entity(search['Labels']):
                    if search['Labels']:
                        category = super()._categorize_entity(search['Labels'])
                        filename = super()._format_filename(search['Name'])
                        output_path = f"{library_search_path}{category}/{filename}"
                        super()._export_data_to_file(output_path, search)

    def _get_scheduled_searches(self) -> None:
        ''' Retrieve current scheduled searches '''
        url = f"{self.url}/scheduledsearches"
        scheduled_search_path= "src/data/scheduled_searches/"
        super()._purge_directory(scheduled_search_path)
        searches = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(scheduled_search_path):
            for search in searches:
                if not super()._check_for_kit_sponsored_entity(search['Labels']):
                    if search['Labels']:
                        category = super()._categorize_entity(search['Labels'])
                        filename = super()._format_filename(search['Name'])
                        output_path = f"{scheduled_search_path}{category}/{filename}"
                        search = super()._delete_variable_search_fields(search)
                        super()._export_data_to_file(output_path, search)

    def _check_for_library_search_changes(self) -> None:
        local_objects = {}
        remote_objects = {}
        url = f"{self.url}/library"
        alert_path= "src/data/library_searches/"
        for search in os.listdir(alert_path):
            for object in os.listdir(f"{alert_path}/{search}"):
                with open(f"{alert_path}/{search}/{object}", 'r') as file_object:
                    file_data = yaml.safe_load(file_object)
                    for key in file_data.keys():
                        local_objects[file_data['ThingUUID']] = search
        searches = super()._execute_get_request(url, self.headers, False)
        if searches:
            for search in searches:
                if not super()._check_for_kit_sponsored_entity(search['Labels']):
                    remote_objects[search['ThingUUID']] = search
            for entry in remote_objects.keys():
                remote_object = remote_objects[entry]
                local_object = local_objects.get(entry, None)
                if local_object is not None:
                    deltas = super()._check_for_deltas(remote_object, local_object)
                    if deltas:
                        url = f"{url}/{entry}"
                        update = super()._execute_put_request(url, self.headers, local_object, False)
                        if update == 200:
                            logging.info("Update operation succeeded for: {0}".format(entry))
                        else:
                            logging.error("Update operation failed for: {0}".format(entry))
        else:
            logging.error("Failed to retrieve remote objects")

    def _check_for_scheduled_search_changes(self) -> None:
        local_objects = {}
        remote_objects = {}
        url = f"{self.url}/scheduledsearches"
        alert_path= "src/data/scheduled_searches/"
        for search in os.listdir(alert_path):
            for object in os.listdir(f"{alert_path}/{search}"):
                with open(f"{alert_path}/{search}/{object}", 'r') as file_object:
                    file_data = yaml.safe_load(file_object)
                    for key in file_data.keys():
                        local_objects[file_data['ID']] = file_data
        searches = super()._execute_get_request(url, self.headers, False)
        if searches:
            for search in searches:
                if not super()._check_for_kit_sponsored_entity(search['Labels']):
                    search = super()._delete_variable_search_fields(search)
                    remote_objects[search['ID']] = search
            for entry in remote_objects.keys():
                remote_object = remote_objects[entry]
                local_object = local_objects.get(entry, None)
                if local_object is not None:
                    deltas = super()._check_for_deltas(remote_object, local_object)
                    if deltas:
                        url = f"{url}/{entry}"
                        update = super()._execute_put_request(url, self.headers, local_object, False)
                        if update == 200:
                            logging.info("Update operation succeeded for: {0}".format(entry))
                        else:
                            logging.error("Update operation failed for: {0}".format(entry))
        else:
            logging.error("Failed to retrieve remote objects")
        