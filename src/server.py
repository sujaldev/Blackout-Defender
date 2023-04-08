import subprocess
from os.path import expanduser
from time import time, sleep

import psutil
from fabric import Connection
from sshconf import read_ssh_config
from wakeonlan import send_magic_packet
from paramiko.ssh_exception import SSHException, NoValidConnectionsError


class Server:
    def __init__(self, mac_address: str, client: str = "proxmox", tick: float = 10, shutdown_delay: float = 4,
                 ping_count: int = 4):
        """
        Main server class.
        :param client: an ssh alias defined in ~/.ssh/config
        :param mac_address: MAC address of the interface on which the Wake on LAN packet should be sent.
        :param tick: Seconds to wait before checking for a state change.
        :param shutdown_delay: Minutes to wait before shutting down the server, after detecting a power outage.
        :param ping_count: Number of pings to perform while checking if host is alive.
        """

        self.client = client
        self.ip = read_ssh_config(expanduser("~/.ssh/config")).host(client)["hostname"]
        # See https://wiki.archlinux.org/title/Wake-on-LAN if you're having trouble with Wake on LAN.
        self.mac_address = mac_address

        self.tick = float(tick)
        self.shutdown_delay = float(shutdown_delay)
        self.ping_count = int(ping_count)

    @property
    def client_is_alive(self) -> bool:
        return subprocess.call(
            ["ping", "-c", str(self.ping_count), str(self.ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        ) == 0

    @property
    def power_state(self) -> bool:
        battery = psutil.sensors_battery()
        if battery is None:
            # Returning True because if you're running this on a machine without a battery, you're probably testing and
            # also if you think about it, on a desktop, battery status is always True ;)
            return True
        return battery.power_plugged

    def execute_shutdown_cmd(self):
        conn = Connection(self.client)
        conn.run("systemctl poweroff", hide=True)
        conn.close()

    def wakeup_client(self):
        send_magic_packet(self.mac_address)

    def shutdown_client(self):
        shutdown_time = time() + self.shutdown_delay * 60

        # Executing shutdown delay
        while time() <= shutdown_time:
            on_mains = self.power_state
            if on_mains:
                return  # power is back, abort shutdown.
            sleep(1)

        self.execute_shutdown_cmd()

        # Waiting for client to shut down, this makes wake up code simple.
        while self.client_is_alive:
            sleep(1)

    def main(self):
        client_alive = self.client_is_alive
        on_mains = self.power_state

        if on_mains and not client_alive:
            self.wakeup_client()
        elif not on_mains and client_alive:
            self.shutdown_client()

    def run(self):
        while True:
            try:
                self.main()
                sleep(self.tick)
            except (SSHException, NoValidConnectionsError):
                continue


if __name__ == "__main__":
    Server("DE:AD:BE:EF").run()
