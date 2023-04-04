from contextlib import redirect_stdout
from multiprocessing import Process, Manager

from cli import *
from tui import TUI
from server import Server


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
        with redirect_stdout(None):
            server_process.start()

        TUI(shared_data).run()
    else:
        server.run()


if __name__ == "__main__":
    main()
