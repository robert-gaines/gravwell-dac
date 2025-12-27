from src.configuration.configuration import Configuration
from src.methods.searches import Searches
from src.methods.alerts import Alerts
import argparse
import logging

logger = logging.basicConfig(level=logging.INFO,
                             format='[%(asctime)s][%(levelname)s][%(message)s]',)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="The Gravwell SIEM API Token")
    arguments = parser.parse_args()
    if arguments.token:
        configuration = Configuration(arguments.token)
        configuration._initialize()
        alerts = Alerts(configuration.headers, configuration.url)
        alerts._check_for_alert_changes()
        alerts._get_alerts()
        searches = Searches(configuration.headers, configuration.url)
        # searches._get_scheduled_searches()
        # searches._check_for_library_search_changes()
        # searches._get_library_searches()
        # searches._check_for_scheduled_search_changes()
        # searches._get_scheduled_searches()



if __name__ == '__main__':
    main()