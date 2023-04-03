import sys
import argparse

__all__ = [
    "CLIENT", "MAC_ADDRESS", "BATTERY_CHECK_INTERVAL", "STATS_CHECK_INTERVAL", "SHUTDOWN_DELAY", "UI"
]

parser = argparse.ArgumentParser(
    prog="bd",
    description="Blackout Defender shuts down your proxmox server connected to a dumb UPS."
)

parser.add_argument(
    "-c", "--client", help="Proxmox host's name as defined in ~/.ssh/config. Make sure to have key-based auth only.",
    default="proxmox"
)

parser.add_argument(
    "-m", "--mac-address", help="Mac address of your proxmox host to send a Wake on Lan packet.", required=True
)

parser.add_argument(
    "-b", "--battery-check-interval", help="Will check for outages at this interval.", type=int
)

parser.add_argument(
    "-f", "--stats-check-interval", help="Will fetch proxmox statistics at this interval.", type=int
)

parser.add_argument(
    "-s", "--shutdown-delay", help="Minutes to wait before shutting down proxmox after detecting an outage.", type=int
)

parser.add_argument(
    "-d", "--no-tui", help="Run as a daemon, will not spawn a TUI.", action="store_true"
)

args = parser.parse_args(sys.argv[1:])

CLIENT = args.client
MAC_ADDRESS = args.mac_address
BATTERY_CHECK_INTERVAL = args.battery_check_interval
STATS_CHECK_INTERVAL = args.stats_check_interval
SHUTDOWN_DELAY = args.shutdown_delay
UI = not args.no_tui
