import subprocess
from time import sleep
from threading import Event, Thread

from cli import *
from data_collector import parse_items

import requests


def call_repeatedly(interval, func, *args, **kwargs):
    stopped = Event()

    def loop():
        while not stopped.wait(interval):
            func(*args, **kwargs)

    Thread(target=loop).start()
    return stopped.set


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.session = requests.Session()

        config = self.get_config()
        self.get_interval = int(config["get_interval"])
        self.post_interval = int(config["post_interval"])
        self.shutdown_delay = int(config["shutdown_delay"])

        self.shutdown_scheduled = False
        self.start()

    @property
    def url(self):
        return f"http://{self.host}" + (f":{self.port}" if self.port != 80 else "")

    def get_config(self) -> dict:
        while True:
            try:
                return requests.get(self.url + "/config").json()
            except (requests.ConnectionError, requests.Timeout):
                sleep(10)

    def post_stats(self) -> None:
        try:
            requests.post(self.url + "/post_stats", data=parse_items())
        except requests.RequestException:
            return

    @property
    def blackout(self) -> bool:
        try:
            return not requests.get(self.url + "/get_battery").content.decode() == 1
        except (requests.ConnectionError, requests.Timeout):
            return True

    def shutdown(self):
        self.shutdown_scheduled = True
        subprocess.run(["shutdown", f"+{self.shutdown_delay}"])

    def cancel_shutdown(self):
        self.shutdown_scheduled = False
        subprocess.run(["shutdown", "-c"])

    def handle_power_status(self):
        if self.blackout:
            if not self.shutdown_scheduled:
                self.shutdown()
        else:
            if self.shutdown_scheduled:
                self.cancel_shutdown()

    def start(self):
        call_repeatedly(self.get_interval, self.handle_power_status)
        call_repeatedly(self.post_interval, self.post_stats)


if __name__ == "__main__":
    Client(HOST, PORT).start()
