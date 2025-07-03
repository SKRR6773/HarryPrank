from check_platform import is_linux
import subprocess
import time
import os


__DIR__ = os.path.dirname(__file__)


FFPLAY_EXECUTABLE_FILENAME = "ffplay" if is_linux else "ffplay.exe"
FFPLAY_PATH = os.path.join(__DIR__, "../ffmpeg", FFPLAY_EXECUTABLE_FILENAME)

MUSIC_TEST_PATH = os.path.join(__DIR__, "../ffmpeg/June.mp3")

# print(os.path.exists(FFPLAY_PATH))



if __name__ == "__main__":
    proc = subprocess.Popen(['-i', MUSIC_TEST_PATH, '-nodisp', '-autoexit'], executable=FFPLAY_PATH)
    # print(proc.stderr.read())


    time.sleep(120)
    # proc.terminate()