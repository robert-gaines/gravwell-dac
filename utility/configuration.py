class Configuration():

    def __init__(self) -> None:
        self.siem = ""
        self.token = ""
        self.headers = {
            "Gravwell-Token": self.token, 
            "Content-Type": "application/json"
        }

        self.query_dir = '../gravwell-siem-config/queries'
        self.alert_dir = '../gravwell-siem-config/alerts'
        self.search_dir = '../gravwell-siem-config/scheduled-searches'

        self.alerts_endpoint = f"https://{self.siem}/api/alerts"
        self.library_endpoint = f"https://{self.siem}/api/library"
        self.searches_endpoint = f"https://{self.siem}/api/scheduledsearches"