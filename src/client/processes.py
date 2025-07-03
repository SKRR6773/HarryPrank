from subprocess import Popen
from logger import logger
from typing import List
import psutil
import os





processes: List[Popen[bytes]] = []



def killALL():
    global processes


    try:

        for proc in processes:
            proc.terminate()
            proc.kill()


    except Exception as ex:
        logger.error(ex)


def killProcessWithName(name: str):
    for proc in psutil.process_iter(['pid', 'name']):
        if name in proc.info['name']:
            proc.kill()


    return True

def killTaskMgr():
    return killProcessWithName("Taskmgr.exe")


