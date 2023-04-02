import sys
import argparse

import defaults

__all__ = [
    "HOST", "PORT", "GET_INTERVAL", "POST_INTERVAL", "SHUTDOWN_DELAY", "NO_TUI"
]

parser = argparse.ArgumentParser(
    prog="blackout-defender",
    description="Gracefully shutdown your proxmox server with a dumb UPS."
)

parser.add_argument(
    "-b", "--host", help="Address to bind to.", default=defaults.HOST
)

parser.add_argument(
    "-p", "--port", help="Port to listen on.", type=int, default=defaults.PORT
)

parser.add_argument(
    "-g", "--get-interval", help="At what interval should the client fetch battery status.", type=int,
    default=defaults.GET_INTERVAL
)

parser.add_argument(
    "-s", "--post-interval", help="At what interval should the client feed the server with client stats.", type=int,
    default=defaults.POST_INTERVAL
)

parser.add_argument(
    "-d", "--shutdown-delay", help="How many minutes to wait before shutting down, after detecting an outage", type=int,
    default=defaults.SHUTDOWN_DELAY
)

parser.add_argument(
    "-n", "--no-tui", help="Starts the server without a TUI.", action="store_true", default=defaults.NO_TUI
)

args = parser.parse_args(sys.argv[1:])

HOST, PORT = args.host, args.port
GET_INTERVAL = args.get_interval
POST_INTERVAL = args.post_interval
SHUTDOWN_DELAY = args.shutdown_delay
NO_TUI = args.no_tui
