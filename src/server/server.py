from __future__ import annotations

import json
import subprocess
from time import sleep, time

from utils import call_repeatedly

import psutil
from fabric import Connection
from paramiko import SSHException
from wakeonlan import send_magic_packet


class Server:
    PING_RETRY_LIMIT = 4
    # seconds to wait before sending a WoL packet to a non-response client (when on mains power)
    # will also be used as the interval to check if the power is back on after a power outage.
    WOL_PACKET_INTERVAL = 10

    SSH_RETRY_LIMIT = 5
    SSH_RETRY_INTERVAL = 10  # in seconds

    BATTERY_CHECK_INTERVAL = 5  # seconds to wait before checking for a power outage.
    STATS_CHECK_INTERVAL = 10  # seconds to wait before fetching new statistics from client.

    SHUTDOWN_DELAY = 4  # how many minutes to wait before shutting down client after detecting an outage
    BATTERY_CHECK_INTERVAL_DURING_SHUTDOWN = 1  # value for BATTERY_CHECK_INTERVAL when a shutdown has been scheduled.

    def __init__(
            self,
            client: str,
            mac_address: str,
            shared_data: dict,
            battery_check_interval: int = None,
            stats_check_interval: int = None,
            shutdown_delay: int = None,
    ):
        """
        This class will run the main process which will perform all the main "protection" functionality, the TUI will
        run in another process and will rely on this process for collecting information to display.

        :param client: Must be a host declared in ~/.ssh/config
        :param mac_address: Mac address of the Wake on Lan interface of the server.
        """

        self.client = client
        self.mac_address = mac_address

        if battery_check_interval is not None:
            self.BATTERY_CHECK_INTERVAL = battery_check_interval
        if stats_check_interval is not None:
            self.STATS_CHECK_INTERVAL = stats_check_interval
        if shutdown_delay is not None:
            self.SHUTDOWN_DELAY = shutdown_delay

        self.connection: Connection | None = None

        # Will be an actual simple dictionary in case ui=False, otherwise `multiprocessing.Manager.dict`.
        self.shared_data: dict = shared_data

        self.kill_stats_loop = None
