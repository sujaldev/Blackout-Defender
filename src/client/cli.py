import sys
import argparse

__all__ = [
    "HOST", "PORT"
]

parser = argparse.ArgumentParser(
    prog="blackout-defender-client",
    description="Gracefully shutdown your proxmox server with a dumb UPS."
)

parser.add_argument(
    "-b", "--host", help="Server's address.", default="0.0.0.0"
)

parser.add_argument(
    "-p", "--port", help="Server's port.", type=int, default=54321
)

args = parser.parse_args(sys.argv[1:])

HOST = args.host
PORT = args.port
