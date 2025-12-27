import logging
import yaml
import os

logger = logging.getLogger()

class Configuration():

    def __init__(self, token: str) -> None:
        self.headers = {
            'Accept': 'application/json',
            'Gravwell-Token': token
        }
        self.fqdn = ""
        self.url = ""

    def _locate_configuration(self) -> None:
        ''' Check for the configuration file '''
        if os.path.exists('src/configuration/configuration.yaml'):
            logger.info("Located configuration")
            return True
        else:
            logger.error("Configuration not present")
            return False
           
    def _parse_configuration(self) -> dict:
        ''' Parse the configuration file '''
        if self._locate_configuration():
            with open('src/configuration/configuration.yaml', 'r') as fobj:
                configuration_data = yaml.safe_load(fobj)
                return configuration_data

    def _check_data_directory_structure(self) -> dict:
        '''
        Iterates through different categories to ensure the directory
        structure is in good order for subsequent operations
        '''
        categories = ['windows',
                      'linux',
                      'network',
                      'hypervisor',
                      'kubernetes']
        category_specific_directories = [
            'alerts',
            'library_searches',
            'scheduled_searches'
        ]
        base_dir = "src/data/"
        for category in category_specific_directories:
            for entry in categories:
                current_directory = f"{base_dir}{category}/{entry}"
                if not os.path.exists(current_directory):
                    try:
                        os.mkdir(current_directory)
                        logger.info("Created directory: {0}".format(current_directory))
                    except Exception as e:
                        logger.exception("Exception raised: {0}".format(e))

    def _initialize(self) -> None:
        ''' Load relevant configuration data '''
        self._check_data_directory_structure()
        configuration = self._parse_configuration()
        self.fqdn = configuration['siem']['fqdn']
        self.url = f"https://{self.fqdn}/api"
        logger.info("Loaded configuration data")