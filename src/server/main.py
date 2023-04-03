from multiprocessing import Process, Manager

from cli import *
from server import Server

from textual.demo import app


def main():
    if UI:
        manager = Manager()
        shared_data = manager.dict()
    else:
        shared_data = {}

    server = Server(
        CLIENT,
        MAC_ADDRESS,
        shared_data,
        BATTERY_CHECK_INTERVAL,
        STATS_CHECK_INTERVAL,
        SHUTDOWN_DELAY
    )

    if UI:
        server_process = Process(target=server.run, daemon=True)
        server_process.start()

        # TODO: implement TUI
        app.run()
    else:
        server.run()


if __name__ == "__main__":
    main()
