from src.configuration.configuration import Configuration
from src.methods.searches import Searches
from src.methods.methods import Methods
from src.methods.alerts import Alerts
import argparse
import logging
import sys

logger = logging.basicConfig(level=logging.INFO,
                             format='[%(asctime)s][%(levelname)s][%(message)s]') # noqa


def sync_all(headers: dict, url: str) -> None:
    searches = Searches(headers, url)
    alerts = Alerts(headers, url)
    searches._check_for_new_library_searches()
    searches._check_for_library_search_changes()
    searches._check_for_new_scheduled_searches()
    searches._check_for_scheduled_search_changes()
    alerts._check_for_new_alerts()
    alerts._check_for_alert_changes()


def main():
    logging.info("Gravwell Detection as Code Utility")
    methods = Methods()
    parser = argparse.ArgumentParser()
    parser.add_argument("--uuid", action='store_true',
                        help="UUID Generation for new object")
    parser.add_argument("--token", help="The Gravwell SIEM API Token")
    parser.add_argument("--lint-directory",
                        help="Lint all files in a directory")
    parser.add_argument("--lint-all-files",
                        action='store_true',
                        help="Lint all files")
    parser.add_argument("--sync-all", action='store_true',
                        help="Execute all non-destructive methods")
    parser.add_argument("--create-alerts",
                        action='store_true',
                        help="Create alerts")
    parser.add_argument("--update-alerts",
                        action='store_true',
                        help="Update alerts")
    parser.add_argument("--delete-alert",
                        help="Delete an alert: run.py --token <token> --delete-alert <id>") # noqa
    parser.add_argument("--list-alerts",
                        action='store_true',
                        help="List alerts")
    parser.add_argument("--get-alerts",
                        action='store_true',
                        help="Export alerts")
    parser.add_argument("--create-library-searches",
                        action='store_true',
                        help="Create library searches")
    parser.add_argument("--update-library-searches",
                        action='store_true',
                        help="Update library searches")
    parser.add_argument("--delete-library-search",
                        help="Delete library search: run.py --token <token> --delete-library-search <id> ") # noqa
    parser.add_argument("--list-library-searches",
                        action='store_true',
                        help="List library searches")
    parser.add_argument("--get-library-searches",
                        action='store_true',
                        help="Export library searches")
    parser.add_argument("--create-scheduled-searches",
                        action='store_true',
                        help="Create scheduled searches")
    parser.add_argument("--update-scheduled-searches",
                        action='store_true',
                        help="Update scheduled searches")
    parser.add_argument("--delete-scheduled-search",
                        help="Delete a scheduled search: run.py --token <token> --delete-scheduled-search <id>") # noqa
    parser.add_argument("--list-scheduled-searches",
                        action='store_true',
                        help="List all scheduled searches")
    parser.add_argument("--get-scheduled-searches",
                        action='store_true',
                        help="Export scheduled searches")
    arguments = parser.parse_args()
    if arguments.lint_directory:
        methods = Methods()
        result = methods._lint_files(arguments.lint_directory)
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
    if arguments.lint_all_files:
        result = False
        directories = [
            'src/data/alerts',
            'src/data/library_searches',
            'src/data/scheduled_searches'
        ]
        methods = Methods()
        for directory in directories:
            result = methods._lint_files(directory)
        if result:
            sys.exit(0)
        else:
            sys.exit(1)
    if arguments.token:
        configuration = Configuration(arguments.token)
        configuration._initialize()
        if arguments.sync_all:
            logging.info("Synchronizing all local configuration data")
            sync_all(configuration.headers,
                     configuration.url)
        if arguments.create_library_searches:
            Searches(configuration.headers,
                     configuration.url)._check_for_new_library_searches()
        if arguments.update_library_searches:
            Searches(configuration.headers,
                     configuration.url)._check_for_library_search_changes()
        if arguments.delete_library_search:
            Searches(configuration.headers,
                     configuration.url)._delete_library_search(
                         arguments.delete_library_search)
        if arguments.list_library_searches:
            Searches(configuration.headers,
                     configuration.url)._list_library_searches()
        if arguments.get_library_searches:
            Searches(configuration.headers,
                     configuration.url)._get_library_searches()
        if arguments.get_scheduled_searches:
            Searches(configuration.headers,
                     configuration.url)._get_scheduled_searches()
        if arguments.create_scheduled_searches:
            Searches(configuration.headers,
                     configuration.url)._check_for_new_scheduled_searches()
        if arguments.update_scheduled_searches:
            Searches(configuration.headers,
                     configuration.url)._check_for_scheduled_search_changes()
        if arguments.list_scheduled_searches:
            Searches(configuration.headers,
                     configuration.url)._list_scheduled_searches()
        if arguments.delete_scheduled_search:
            Searches(configuration.headers,
                     configuration.url)._delete_scheduled_search(
                         arguments.delete_scheduled_search)
        if arguments.create_alerts:
            Alerts(configuration.headers,
                   configuration.url)._check_for_new_alerts()
        if arguments.update_alerts:
            Alerts(configuration.headers,
                   configuration.url)._check_for_alert_changes()
        if arguments.delete_alert:
            Alerts(configuration.headers,
                   configuration.url)._delete_alert(arguments.delete_alert)
        if arguments.list_alerts:
            Alerts(configuration.headers,
                   configuration.url)._list_alerts()
        if arguments.get_alerts:
            Alerts(configuration.headers,
                   configuration.url)._get_alerts()
        if arguments.uuid:
            uuid = methods._generate_uuid()
            logging.info(f"UUID:{uuid}")
    if not arguments.token and not arguments.lint_all_files \
            and not arguments.lint_directory:
        parser.print_help()


if __name__ == '__main__':
    main()
