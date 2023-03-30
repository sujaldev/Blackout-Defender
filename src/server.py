import json
import socket
import logging
from time import sleep
from threading import Thread, Event

logging.basicConfig(level=logging.DEBUG)


# logging.getLogger().disabled = True


class Server:
    HOST = "0.0.0.0"
    PORT = 43210
    UPDATE_INTERVAL = b"5"  # in seconds

    def __init__(self, host: str = None, port: int = None, update_interval: int = None):
        self.host = host or self.HOST
        self.port = port or self.PORT
        self.update_interval = str(update_interval).encode() or self.UPDATE_INTERVAL

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        logging.info("Server Listening...")

        # Is set to true when new data is received from the client, set to false again when updated in the TUI
        self.new_data = False
        self.data = None

        self._running = Event()  # For a graceful shutdown
        self._running.set()

    def run(self) -> None:
        """
        Starts the server and waits for one and only one client to connect, will not handle multiple data sources by
        design (of *my* network/servers, feel free to change it according to yours).
        """
        while self._running:
            conn, addr = self.sock.accept()
            logging.info(f"Received connection from '{addr[0]}:{addr[-1]}'")

            with conn:
                conn.sendall(self.UPDATE_INTERVAL)
                logging.debug("Sent update interval config to connected client.")
                self.recv_loop(conn)

    def recv_loop(self, conn: socket.socket) -> None:
        logging.info("Starting recv loop...")
        conn.settimeout(1.0)
        while self._running:
            logging.info(f"Run shared bool: {bool(self._running)}")
            try:
                self.data = conn.recv(4096)
                self.new_data = True
                logging.debug(f"Received data: '{self.data.decode()}'")
            except socket.timeout:
                logging.debug("recv timeout")
                continue

    def read(self) -> dict | None:
        """
        Called by the TUI to read for new data at configured interval
        """
        if not self.new_data:
            return None

        sleep(1)  # Tolerance for a slightly delayed recv
        self.new_data = False
        return json.loads(self.data)

    def quit(self) -> None:
        logging.info("Quiting...")
        self._running.clear()


if __name__ == "__main__":
    server = Server()
    server_thread = Thread(target=server.run)
    server_thread.start()

    for _ in range(5):
        logging.info(f"Client read: '{server.read()}'")
        sleep(5)

    server.quit()
