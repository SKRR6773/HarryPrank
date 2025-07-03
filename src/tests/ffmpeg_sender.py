import subprocess
import socket
import os



__DIR__ = os.path.dirname(__file__)


FFMPEG_PATH = os.path.join(__DIR__, "../ffmpeg/ffmpeg")
SONG_PATH = os.path.join(__DIR__, "../ffmpeg/June.mp3")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.bind(('', 6774))
server.listen(1)


client, addr = server.accept()


# ffmpeg = subprocess.Popen([FFMPEG_PATH, '-i', SONG_PATH, '-f', "s16le", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", "pipe:1"], stdout=subprocess.PIPE)
ffmpeg = subprocess.Popen([FFMPEG_PATH, '-f', 'x11grab', '-i', ":0.0", '-f', "alsa", "-i", "default", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-f", "nut", "pipe:1"], stdout=subprocess.PIPE)

while True:
    try:
        data = ffmpeg.stdout.read(4096)


        if not data:
            break


        
        client.sendall(data)
        # print(data)
        
        # ffmpeg.kill()
        # break

    except KeyboardInterrupt:
        break



ffmpeg.terminate()
client.close()
server.close()