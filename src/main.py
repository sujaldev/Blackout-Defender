from cli import *
from server import Server

if __name__ == "__main__":
    Server(MAC_ADDRESS, CLIENT, TICK, SHUTDOWN_DELAY, PING_COUNT).run()
