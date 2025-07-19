from utils.env import HELLOCLIENT_PORT
from client.logger import logger, info
import socket


class HandShake:
    def __init__(self):
        self.is_running = True
        self.server_ip: str = None


        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server.bind(('', HELLOCLIENT_PORT))
        self.server.settimeout(3)


    def listening(self):
        while self.is_running:
            try:
                if not self.server:
                    break


                if self.server_ip:
                    break


                data, addr = self.server.recvfrom(1024)

                info(addr)


                data_decoded = data.decode(errors='ignore')

                socket.inet_aton(data_decoded)

                self.server_ip = data_decoded



            except KeyboardInterrupt:
                self.is_running = False
                break


            except TimeoutError:
                info("Retry again")
                continue

            except Exception as ex:
                logger.error(ex)



        self.close()




    @property
    def serverIP(self):
        return self.server_ip
    


    def close(self):
        if self.is_running:
            try:
                self.server.close()

            except:
                pass

            
            self.server = None
            self.is_running = False
            