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
        library_search_path = "src/data/library_searches/"
        super()._purge_directory(library_search_path)
        searches = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(library_search_path):
            for search in searches:  # type: ignore
                if not super()._check_for_kit_sponsored_entity(search['Labels']): # noqa
                    if search['Labels']:
                        category = super()._categorize_entity(search['Labels'])
                        filename = super()._format_filename(search['Name'])
                        output_path = f"{library_search_path}{category}/{filename}" # noqa
                        super()._export_data_to_file(output_path, search)

    def _check_for_library_search_changes(self) -> None:
        ''' Identify changes in library search definitions '''
        local_objects = {}
        remote_objects = {}
        url = f"{self.url}/library"
        search_path = "src/data/library_searches/"
        for search in os.listdir(search_path):
            for object in os.listdir(f"{search_path}/{search}"):
                with open(f"{search_path}/{search}/{object}", 'r') as file_object: # noqa
                    file_data = yaml.safe_load(file_object)
                    for key in file_data.keys():
                        local_objects[file_data['ThingUUID']] = file_data
        searches = super()._execute_get_request(url, self.headers, False)
        if searches:
            for search in searches:  # type: ignore
                if not super()._check_for_kit_sponsored_entity(search['Labels']): # noqa
                    remote_objects[search['ThingUUID']] = search
            for entry in remote_objects.keys():
                remote_object = remote_objects[entry]
                local_object = local_objects.get(entry, None)
                if local_object is not None:
                    deltas = super()._check_for_deltas(remote_object,
                                                       local_object)
                    if deltas:
                        url = f"{url}/{entry}"
                        update = super()._execute_put_request(url,
                                                              self.headers,
                                                              local_object,
                                                              False)
                        if update == 200:
                            logging.info(f"Update operation succeeded for: {entry}") # noqa
                            self._get_library_searches()
                        else:
                            logging.error(f"Update operation failed for: {entry}") # noqa
        else:
            logging.error("Failed to retrieve remote objects")

    def _check_for_new_library_searches(self) -> None:
        ''' Check for newly authored library searches '''
        local_objects = {}
        remote_objects = {}
        url = f"{self.url}/library"
        alert_path = "src/data/library_searches"
        for entry in os.listdir(alert_path):
            for object in os.listdir(f"{alert_path}/{entry}"):
                with open(f"{alert_path}/{entry}/{object}", 'r') as file_object: # noqa
                    file_data = yaml.safe_load(file_object)
                    for key in file_data.keys():
                        local_objects[file_data['GUID']] = file_data
        library_searches = super()._execute_get_request(url,
                                                        self.headers,
                                                        False)
        if library_searches:
            for search in library_searches:  # type: ignore
                if not super()._check_for_kit_sponsored_entity(search['Labels']): # noqa
                    remote_objects[search['GUID']] = search
            for entry in local_objects.keys():
                local_object = remote_objects.get(entry, None)
                if local_object is None:
                    search_payload = local_objects[entry]
                    create = super()._execute_post_request(url,
                                                           self.headers,
                                                           search_payload,
                                                           False)
                    if create == 200:
                        logging.info(f"Library search creation succeeded for: {entry}") # noqa
                        self._get_library_searches()
                    else:
                        logging.error(f"Library search creation failed for: {entry}") # noqa
        else:
            logging.error("Failed to retrieve remote objects")

    def _list_library_searches(self) -> None:
        '''List current library searches'''
        url = f"{self.url}/library"
        library_searches = super()._execute_get_request(url,
                                                        self.headers,
                                                        False)
        if library_searches:
            for search in library_searches:  # type: ignore
                logging.info(f"{search['ThingUUID']}:{search['Name']}")
        else:
            logging.error("Failed to retrieve library searches")

    def _delete_library_search(self, library_search_id: str) -> None:
        ''' Delete given library search '''
        url = f"{self.url}/library/{library_search_id}"
        delete = super()._execute_delete_request(url, self.headers, False)
        if delete == 200:
            logging.info(f"Library search removal succeeded for: {library_search_id}") # noqa
            self._get_library_searches()
        else:
            logging.error(f"Library search removal failed for: {library_search_id}") # noqa

    def _get_scheduled_searches(self) -> None:
        ''' Retrieve current scheduled searches '''
        url = f"{self.url}/scheduledsearches"
        scheduled_search_path = "src/data/scheduled_searches/"
        super()._purge_directory(scheduled_search_path)
        searches = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(scheduled_search_path):
            for search in searches:  # type: ignore
                if not super()._check_for_kit_sponsored_entity(search['Labels']): # noqa
                    if search['Labels']:
                        category = super()._categorize_entity(search['Labels'])
                        filename = super()._format_filename(search['Name'])
                        output_path = f"{scheduled_search_path}{category}/{filename}" # noqa
                        search = super()._delete_variable_search_fields(search)
                        super()._export_data_to_file(output_path, search)

    def _check_for_scheduled_search_changes(self) -> None:
        ''' Check for changes in schedule search definitions '''
        local_objects = {}
        remote_objects = {}
        url = f"{self.url}/scheduledsearches"
        search_path = "src/data/scheduled_searches/"
        for search in os.listdir(search_path):
            for object in os.listdir(f"{search_path}/{search}"):
                with open(f"{search_path}/{search}/{object}", 'r') as file_object: # noqa
                    file_data = yaml.safe_load(file_object)
                    for key in file_data.keys():
                        local_objects[file_data['ID']] = file_data
        searches = super()._execute_get_request(url, self.headers, False)
        if searches:
            for search in searches:   # type: ignore
                if not super()._check_for_kit_sponsored_entity(search['Labels']): # noqa
                    search = super()._delete_variable_search_fields(search)
                    remote_objects[search['ID']] = search
            for entry in remote_objects.keys():
                remote_object = remote_objects[entry]
                local_object = local_objects.get(entry, None)
                if local_object is not None:
                    deltas = super()._check_for_deltas(remote_object,
                                                       local_object)
                    if deltas:
                        url = f"{url}/{entry}"
                        update = super()._execute_put_request(url,
                                                              self.headers,
                                                              local_object,
                                                              False)
                        if update == 200:
                            logging.info(f"Update operation succeeded for: {entry}") # noqa
                            self._get_scheduled_searches()
                        else:
                            logging.error("Update operation failed for: {entry}") # noqa
        else:
            logging.error("Failed to retrieve remote objects")

    def _check_for_new_scheduled_searches(self) -> None:
        ''' Identify new scheduled search definitions '''
        local_objects = {}
        remote_objects = {}
        url = f"{self.url}/scheduledsearches"
        alert_path = "src/data/scheduled_searches/"
        for entry in os.listdir(alert_path):
            for object in os.listdir(f"{alert_path}/{entry}"):
                with open(f"{alert_path}/{entry}/{object}", 'r') as file_object: # noqa
                    file_data = yaml.safe_load(file_object)
                    for key in file_data.keys():
                        local_objects[file_data['GUID']] = file_data
        scheduled_searches = super()._execute_get_request(url,
                                                          self.headers,
                                                          False)
        if scheduled_searches:
            for search in scheduled_searches:  # type: ignore
                if not super()._check_for_kit_sponsored_entity(search['Labels']): # noqa
                    remote_objects[search['GUID']] = search
            for entry in local_objects.keys():
                local_object = remote_objects.get(entry, None)
                if local_object is None:
                    search_payload = local_objects[entry]
                    create = super()._execute_post_request(url,
                                                           self.headers,
                                                           search_payload,
                                                           False)
                    if create == 200:
                        logging.info(f"Scheduled search creation succeeded for: {entry}") # noqa
                        self._get_scheduled_searches()
                    else:
                        logging.error(f"Scheduled search creation failed for: {entry}") # noqa
        else:
            logging.error("Failed to retrieve remote objects")

    def _list_scheduled_searches(self) -> None:
        ''' List current scheduled searches '''
        url = f"{self.url}/scheduledsearches"
        scheduled_searches = super()._execute_get_request(url,
                                                          self.headers,
                                                          False)
        if scheduled_searches:
            for search in scheduled_searches:  # type: ignore
                logging.info(f"{search['ID']}:{search['Name']}")
        else:
            logging.error("Failed to retrieve scheduled searches")

    def _delete_scheduled_search(self, scheduled_search_id: str) -> None:
        ''' Delete a given scheduled search '''
        url = f"{self.url}/scheduledsearches/{scheduled_search_id}"
        delete = super()._execute_delete_request(url, self.headers, False)
        if delete == 200:
            logging.info(f"Scheduled search removal succeeded for: {scheduled_search_id}") # noqa
            self._get_scheduled_searches()
        else:
            logging.error(f"Scheduled search removal failed for: {scheduled_search_id}") # noqa