from utils.env import HELLOCLIENT_PORT, BROADCAST_INTERTIME
from utils.check_ips import IPV4
from server.logger import info
import socket
import time





class HelloClient:
    def __init__(self):
        self.is_running = True


        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)



    def broadcast(self):
        while self.is_running:
            info(f"Broadcast to everyone with {IPV4}")
            self.server.sendto(IPV4.encode(), ("<broadcast>", HELLOCLIENT_PORT))

            time.sleep(BROADCAST_INTERTIME)


        self.close()


    def close(self):
        if self.is_running:
            self.server.close()
            self.is_running = False


            info("HelloClient is closed")



