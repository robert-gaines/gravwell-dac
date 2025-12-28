from src.configuration.configuration import Configuration
from src.methods.searches import Searches
from src.methods.methods import Methods
from src.methods.alerts import Alerts
import argparse
import logging

logger = logging.basicConfig(level=logging.INFO,
                             format='[%(asctime)s][%(levelname)s][%(message)s]',)

def main():
    logging.info("Gravwell Detection as Code Utility")
    methods = Methods()
    parser = argparse.ArgumentParser()
    parser.add_argument("--uuid", action='store_true' , help="UUID Generation for new object")
    parser.add_argument("--token", help="The Gravwell SIEM API Token")
    parser.add_argument("--sync-all", action='store_true', help="Execute all non-destructive methods")
    parser.add_argument("--create-alerts", action='store_true', help="Create alerts")
    parser.add_argument("--update-alerts", action='store_true', help="Update alerts")
    parser.add_argument("--delete-alert", help="Delete an alert: run.py --token <token> --delete-alert <id>")
    parser.add_argument("--list-alerts", action='store_true', help="List alerts")
    parser.add_argument("--get-alerts", action='store_true', help="Export alerts")
    parser.add_argument("--create-library-searches", action='store_true', help="Create library searches")
    parser.add_argument("--update-library-searches", action='store_true', help="Update library searches")
    parser.add_argument("--delete-library-search", help="Delete library search: run.py --token <token> --delete-library-search <id> ")
    parser.add_argument("--list-library-searches", action='store_true', help="List library searches")
    parser.add_argument("--get-library-searches", action='store_true', help="Export library searches")
    parser.add_argument("--create-scheduled-searches", action='store_true', help="Create scheduled searches")
    parser.add_argument("--update-scheduled-searches", action='store_true', help="Update scheduled searches")
    parser.add_argument("--delete-scheduled-search", help="Delete a scheduled search: run.py --token <token> --delete-scheduled-search <id>")
    parser.add_argument("--list-scheduled-searches", action='store_true', help="List all scheduled searches")
    parser.add_argument("--get-scheduled-searches", action='store_true', help="Export scheduled searches")
    arguments = parser.parse_args()
    if arguments.token:
        configuration = Configuration(arguments.token)
        configuration._initialize()
        alerts = Alerts(configuration.headers, configuration.url)
        searches = Searches(configuration.headers, configuration.url)
        if arguments.sync_all:
            logging.info("Synchronizing all local configuration data")
            searches._check_for_new_library_searches()
            searches._check_for_library_search_changes()
            searches._check_for_new_scheduled_searches()
            searches._check_for_scheduled_search_changes()
            alerts._check_for_new_alerts()
            alerts._check_for_alert_changes()
        if arguments.create_library_searches:
            searches._check_for_new_library_searches()
        if arguments.update_library_searches:
            searches._check_for_library_search_changes()
        if arguments.delete_library_search:
            searches._delete_library_search(arguments.delete_library_search)
        if arguments.list_library_searches:
            searches._list_library_searches()
        if arguments.get_library_searches:
            searches._get_library_searches()
        if arguments.get_scheduled_searches:
            searches._get_scheduled_searches()
        if arguments.create_scheduled_searches:
            searches._check_for_new_scheduled_searches()
        if arguments.update_scheduled_searches:
            searches._check_for_scheduled_search_changes()
        if arguments.list_scheduled_searches:
            searches._list_scheduled_searches()
        if arguments.delete_scheduled_search:
            searches._delete_scheduled_search(arguments.delete_scheduled_search)
        if arguments.create_alerts:
            alerts._check_for_new_alerts()
        if arguments.update_alerts:
            alerts._check_for_alert_changes()
        if arguments.delete_alert:
            alerts._delete_alert(arguments.delete_alert)
        if arguments.list_alerts:
            alerts._list_alerts()
        if arguments.get_alerts:
            alerts._get_alerts()
    if arguments.uuid:
        uuid = methods._generate_uuid()
        logging.info(f"UUID:{uuid}")



if __name__ == '__main__':
    main()