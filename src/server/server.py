# Server.py
from Client import _Client, Client
from logger import info, logger
from threading import Thread
from env import SERVER_PORT
from typing import List
import socket
import uuid






class Server:
    def __init__(self):
        self.is_running = True

        self.clients: List[_Client] = []        # Client ที่ไม่ใช่ socket object 


        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', SERVER_PORT))
        self.server.listen(10)
        self.server.settimeout(5)



    def listening(self):
        info("Server Listening...")


        while self.is_running:
            try:
                __client, addr = self.server.accept()


                _client = Client(__client, addr)
                _client.setUUID(self.getClientUUID)
                _client.setOnCloseCallback(lambda: self.onClose(_client))

                client = _Client(_client, addr)
                
                task = Thread(target=_client.listening, args=())
                task.start()
                client.task = task

                self.clients.append(client)


            except TimeoutError:
                continue


            except Exception as ex:
                logger.error(ex)

        
        self.close()


    def onClose(self, client: Client):
        index = -1

        for i, _client in enumerate(self.clients):
            if _client.client.uuid == client.uuid:
                index = i
                break

        
        if index != -1:
            self.clients.pop(index)


    def close(self):
        if self.is_running:

            # close all client session
            for client in self.clients:
                client.client.close()


            self.clients.clear()
            self.server.close()
            self.is_running = False

            info("Server TCP is Closed")



    def findClientWithClientUUID(self, client_uuid: str) -> Client | None:
        for client in self.clients:
            if client.client.uuid == client_uuid:
                return client.client
            

        return None


    @property
    def getAllClient(self):
        return map(lambda e: e.client, self.clients)
    

    @property
    def getAllClientUUID(self):
        return map(lambda e: e.uuid, self.getAllClient)
    

    @property
    def getClientUUID(self):
        while True:
            v4 = str(uuid.uuid4())

            if v4 not in self.getAllClientUUID:
                return v4
            




