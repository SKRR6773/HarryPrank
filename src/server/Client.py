from utils.packer import parsePackV1, Pack, CommandTypes, packV1, ContentTypes
from typing import List, Any, Callable
from dataclasses import dataclass
from server.logger import info, logger
from threading import Thread
from utils.env import SPLITTER
import server.closeServe as closeServe
import server.shared as shared
import socket
import shlex


class Client:
    def __init__(self, client: socket.socket, addr):
        self.is_running = True
        self._buffer = b''
        self.is_admin: bool = False
        self.custom_name: str = None
        self.description: str = None
        self.data: dict = {}
        self.uuid: str = None

        self.ping_late: int = 0

        self.__on_close__: Callable = None
        

        self.client = client
        self.addr = addr
        self.client.settimeout(10)

        info(f"Client Join: " + str(addr))
        self.sendData("GetComputerInfo", ContentTypes.STR, None, None, None, None)


    def setUUID(self, uuid: str):
        self.uuid = uuid
        self.sendData("SetUUID", ContentTypes.STR, uuid, None, None, None)


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
                if self.ping_late > 3:
                    break


                self.sendPing()
                self.ping_late += 1
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
            


        except ModuleNotFoundError:
            logger.error("Client sent CommandType Not Found")
            pass


    def onServerCommand(self, command: Pack):
        

        if command.name == "ListClient":
            self.sendData("ClientList", ContentTypes.JSON, list(shared.server.getAllClientUUID), command.ref_id, None)

        elif command.name == "SERV_STOP":
            closeServe.closeServ()


        else:
            self.send404Command(command)



    def onSelectTarget(self, command: Pack):

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


            _client = shared.server.findClientWithClientUUID(_user_uuid)


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


                elif first_command == "GET_LOG":
                    _client.sendData("GET_LOG", ContentTypes.STR, "", command.ref_id, command.command_type, command.from_sender)


        # if True:
        #     pass


        # else:
        #     self.send404Command(command)


    def onCommonCommand(self, command: Pack):   # Client Response
        # print(command)


        if command.name == "ComputerInfo":          
            self.data['ComputerInfo'] = command.data

        
        elif command.name == "UpRole":
            if command.data == "ADMIN":
                self.is_admin = True

            else:
                self.sendErrorCommand(command, "Not found role")

        
        elif command.name == "LOG_RESPONSE":
            pass        # ไม่ให้เข้า 404


        elif command.name == "PONG":
            self.ping_late = 0

        else:
            self.send404Command(command)



        if command.from_sender:
            self.sendToUUID(command.from_sender, command)


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


    def sendToUUID(self, uuid: str, command: Pack):
        if shared.server:
            client = shared.server.findClientWithClientUUID(uuid)


            if client:
                client.sendData(command.name, command.content_type, command.data, command.ref_id, command.command_type, self.uuid)
                


    def sendPing(self):
        self.sendData("PING", ContentTypes.STR, "", None, CommandTypes.SERVER_COMMAND, None)


    def close(self):
        if shared.is_running:
            info(f"Client {self.addr} Disconnection")
            self._buffer = b''

            try:
                self.client.close()
                self.client.shutdown(socket.SHUT_RDWR)

            except:
                pass


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