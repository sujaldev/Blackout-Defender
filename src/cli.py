import sys
import argparse

__all__ = [
    "MAC_ADDRESS", "CLIENT", "TICK", "SHUTDOWN_DELAY", "PING_COUNT"
]

parser = argparse.ArgumentParser(
    prog="bd-server",
    description="Blackout Defender shuts down your proxmox server connected to a dumb UPS."
)

parser.add_argument(
    "-m", "--mac-address",
    help="MAC address of the interface on which the Wake on LAN packet should be sent. This is usually going to be "
         "the mac address of your proxmox server's motherboard's NIC, even if you have one connected via PCIE.",
    required=True
)

parser.add_argument(
    "-c", "--client", help="Proxmox's ssh alias as defined in ~/.ssh/config. Make sure to have key-based auth only.",
    default="proxmox"
)

parser.add_argument(
    "-t", "--tick", help="Seconds to wait before checking for a state change.", type=float, default=10
)

parser.add_argument(
    "-s", "--shutdown-delay", help="Minutes to wait before shutting down proxmox after detecting an outage.",
    type=float, default=4
)

parser.add_argument(
    "-p", "--ping-count", help="Number of pings to send to determine whether client is alive or not.", type=int,
    default=4,
)

args = parser.parse_args(sys.argv[1:])

MAC_ADDRESS = args.mac_address
CLIENT = args.client
TICK = args.tick
SHUTDOWN_DELAY = args.shutdown_delay
PING_COUNT = args.ping_count
