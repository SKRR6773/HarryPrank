from threading import Thread
from dataclasses import dataclass
import subprocess
import requests
import socket
import os


__DIR__ = os.path.dirname(__file__)


END_POINT = "http://s6773code.thddns.net:8999/api/public/harry_prank"
VERSION_PATH = os.path.join(__DIR__, "version.txt")


@dataclass
class Conf:
    executable: str
    port: int


DEFAULT_CONF: Conf = Conf(**{
    "executable": "",
    "port": 6777
})



class Main:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', DEFAULT_CONF.port))
        self.server.listen(1)

        

        self.server.close()


    def run(self):
        pass

    def runMainApp(self):
        subprocess.Popen()


    def listeningCheck(self):
        pass


    def getCurrentVersion():
        if not os.path.exists(VERSION_PATH):
            return None
        

        with open(VERSION_PATH, 'r', encoding="utf-8")as fr:
            return fr.read().strip()
        

    def checkUpdate():
        with requests.get(END_POINT + "/version.txt", timeout=10)as req:
            print(req.text.strip())


if __name__ == "__main__":
    main = Main()

    task = Thread(target=main.run, args=())
    task.start()
    task.join()