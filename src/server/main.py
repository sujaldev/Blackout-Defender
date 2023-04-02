from queue import Queue
from threading import Thread

from cli import *
from tui import TUI
from server import create_app

# Will be used by the TUI thread to read new data, and by the server thread to write new data.
STATS_QUEUE = Queue()


def start_server():
    create_app(
        STATS_QUEUE, GET_INTERVAL, POST_INTERVAL, SHUTDOWN_DELAY
    ).run(
        HOST, PORT, debug=False
    )


def main():
    if NO_TUI:
        start_server()
    else:
        thread = Thread(target=start_server, daemon=True)
        thread.start()
        TUI().run()


if __name__ == "__main__":
    main()
