import requests
import time

from prometheus_client import start_http_server, Gauge
from urllib3.exceptions import InsecureRequestWarning

server_port = 10000


def start_monitoring():
    trueconf_units = Gauge('trueconf_units', 'Number of active units', ['unit'])

    update_interval = 15
    api_endpoint_users = "https://127.0.0.1/api/v3.1/users"
    api_endpoint_conferences = "https://127.0.0.1/api/v3.1/conferences"
    api_key = "your_access_token"
    api_page_size = 500
    api_params = {"access_token": api_key, "page_size": api_page_size}
    units = [api_endpoint_users, api_endpoint_conferences]

    while True:
        user_counter = 0
        conferences_counter = 0

        for unit in units:
            response = requests.get(url=unit, params=api_params, verify=False)
            data = response.json()

            if "users" in unit:
                users_list = data["users"]
                for user in users_list:
                    if user["status"] in [1, 2, 5]:
                        user_counter += 1
            elif "conferences" in unit:
                conferences_list = data["conferences"]
                for conference in conferences_list:
                    if conference["state"] == "running":
                        conferences_counter += 1

        trueconf_units.labels("USERS").set(user_counter)
        trueconf_units.labels("CONFERENCES").set(conferences_counter)
        time.sleep(update_interval)


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    start_http_server(server_port)
    start_monitoring()
