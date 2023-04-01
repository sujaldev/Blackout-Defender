from ast import literal_eval
from fabric import Connection, Result


class Client:
    def __init__(self, host: str = "proxmox"):
        """
        In the spirit of being lazy and keeping it simple, do all your fancy ssh-fu in the config file and just pass the
        host parameter here.
        :param host: A host in your ~/.ssh/config file (not necessarily though)
        """
        self.connection = Connection(host)

    @property
    def stats(self) -> dict:
        """
        You need to have the `src/data_collector.py` file placed in your client's `/usr/bin` directory (or any other
        directory in PATH) and rename the file to `duas-client-data`.
        """
        return literal_eval(self.connection.run("duas-client-data").stdout)

    def shutdown(self) -> Result:
        return self.connection.run("systemctl poweroff")
