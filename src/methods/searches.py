from src.methods.methods import Methods
import logging
import yaml

logger = logging.getLogger()

class Searches(Methods):

    def __init__(self, headers: dict, url: str) -> None:
        self.headers = headers
        self.url = url
        super().__init__()
    
    def _get_library_searches(self) -> None:
        url = f"{self.url}/library"
        alert_path= "src/data/library_searches/"
        searches = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(alert_path):
            for search in searches:
                if not super()._check_for_kit_sponsored_entity(search['Labels']):
                    if search['Labels']:
                        category = super()._categorize_entity(search['Labels'])
                        filename = super()._format_filename(search['Name'])
                        output_path = f"{alert_path}{category}/{filename}"
                        super()._export_data_to_file(output_path, search)

    def _get_scheduled_searches(self) -> None:
        url = f"{self.url}/scheduledsearches"
        alert_path= "src/data/scheduled_searches/"
        searches = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(alert_path):
            for search in searches:
                if not super()._check_for_kit_sponsored_entity(search['Labels']):
                    if search['Labels']:
                        category = super()._categorize_entity(search['Labels'])
                        filename = super()._format_filename(search['Name'])
                        output_path = f"{alert_path}{category}/{filename}"
                        super()._export_data_to_file(output_path, search)