from src.methods.methods import Methods
import logging
import yaml

logger = logging.getLogger()

class Alerts(Methods):

    def __init__(self, headers: dict, url: str) -> None:
        self.headers = headers
        self.url = url
        super().__init__()
    
    def _get_alerts(self) -> None:
        url = f"{self.url}/alerts"
        alert_path= "src/data/alerts/"
        alerts = super()._execute_get_request(url, self.headers, False)
        if super()._check_directory_path(alert_path):
            for alert in alerts:
                category = super()._categorize_entity(alert['Labels'])
                filename = super()._format_filename(alert['Name'])
                output_path = f"{alert_path}{category}/{filename}"
                super()._export_data_to_file(output_path, alert)