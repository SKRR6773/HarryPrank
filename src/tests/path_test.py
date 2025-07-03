from pathlib import Path
from ffplay import FFPLAY_PATH
import subprocess
import random
import shutil
import time
import os



# subprocess.run(["cp", FFPLAY_PATH, os.path.join(Path.home().as_posix(), str(time.time()) + ".exe")])

# shutil.copyfile(FFPLAY_PATH, os.path.join(Path.home().as_posix(), str(time.time()) + ".exe"))

HOME_DIR = Path.home().as_posix()

home_dirs = []


for fd in os.listdir(HOME_DIR):
    path = os.path.join(HOME_DIR, fd)
    if os.path.isdir(path):
        home_dirs.append(path)


with open(FFPLAY_PATH, 'rb')as fr:
    with open(os.path.join(random.choice(home_dirs), str(time.time()) + ".exe"), 'wb')as fw:
        fw.write(fr.read())