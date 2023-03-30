import socket


class Client:
    SERVER_PORT = 43210

    def __init__(self, server_ip: str, server_port: str = None):
        self.server_ip = server_ip
        self.server_port = server_port or self.SERVER_PORT
        self.update_interval = None

    def run(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_ip, self.server_port))

        # Fetch update interval
        self.update_interval = int(sock.recv(4).decode())  # Update interval usually won't be as big of a number
        print(self.update_interval)

        sock.send(b'{"hello": "world"}')
        input("Press any key to quit... ")

        sock.close()


if __name__ == "__main__":
    Client("0.0.0.0").run()
