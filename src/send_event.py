from configparser import ConfigParser
import requests

EVENT_RUN_STARTED = "run-started"
EVENT_RUN_FINISHED = "run-finished"

class _EventsHelper():
    def __init__(self):
        config = self.__read_config()
        self.auth_token = config.get("auth", "token")
        self.event_endpoints = {
            EVENT_RUN_STARTED: [],
            EVENT_RUN_FINISHED: [],
        }

        for entry in config.items("events"):
            event_name = entry[0].split("--")[0]
            if (event_name in self.event_endpoints):
                self.event_endpoints[event_name].append(entry[1])

    def __read_config(self):
        parser = ConfigParser()
        parser.read("events.ini")
        return parser

    def send_event(self, event, data={}):
        if (event in self.event_endpoints):
            data["event"] = event
            for endpoint in self.event_endpoints[event]:
                try:
                    resp = requests.post(endpoint, json=data, headers={"Authorization": "Bearer " + self.auth_token})
                    if (not resp.ok):
                        raise Exception("Received status code " + str(resp.status_code))
                except Exception as e:
                    print("Failed to send event to " + endpoint + ", Error:", e)

eventsHelper = _EventsHelper()
