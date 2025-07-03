import socket
import subprocess


# ffplay = subprocess.Popen(['ffplay', '-f', 's16le', '-ar', '44100', '-ac', '2', '-autoexit', '-i', 'pipe:0'], stdin=subprocess.PIPE)
ffplay = subprocess.Popen(['ffplay', '-f', 'nut', '-autoexit', '-i', 'pipe:0'], stdin=subprocess.PIPE)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('192.168.1.102', 6774))



while True:
    try:
        data = server.recv(4096)


        if not data:
            break


        # print(data)

        ffplay.stdin.write(data)


    except KeyboardInterrupt:
        break

    

ffplay.terminate()
server.close()