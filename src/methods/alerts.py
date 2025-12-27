from src.methods.methods import Methods
import logging
import yaml
import os

logger = logging.getLogger()

class Alerts(Methods):

    def __init__(self, headers: dict, url: str) -> None:
        self.headers = headers
        self.url = url
        super().__init__()

    def _get_alerts(self) -> None:
        ''' Retrieve current alerts and export to YAML '''
        url = f"{self.url}/alerts"
        alert_path= "src/data/alerts/"
        super()._purge_directory(alert_path)
        alerts = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(alert_path):
            for alert in alerts:
                if not super()._check_for_kit_sponsored_entity(alert['Labels']):
                    if alert['Labels']:
                        category = super()._categorize_entity(alert['Labels'])
                        filename = super()._format_filename(alert['Name'])
                        output_path = f"{alert_path}{category}/{filename}"
                        super()._export_data_to_file(output_path, alert)

    def _check_for_alert_changes(self) -> None:
        local_objects = {}
        remote_objects = {}
        url = f"{self.url}/alerts"
        alert_path= "src/data/alerts/"
        for entry in os.listdir(alert_path):
            for object in os.listdir(f"{alert_path}/{entry}"):
                with open(f"{alert_path}/{entry}/{object}", 'r') as file_object:
                    file_data = yaml.safe_load(file_object)
                    for key in file_data.keys():
                        local_objects[file_data['ThingUUID']] = file_data
        alerts = super()._execute_get_request(url, self.headers, False)
        if alerts:
            for alert in alerts:
                if not super()._check_for_kit_sponsored_entity(alert['Labels']):
                    remote_objects[alert['ThingUUID']] = alert
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