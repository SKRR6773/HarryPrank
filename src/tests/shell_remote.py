import subprocess


while True:
    try:
        cmd = input(">")


        if cmd == "exit":
            break


        subprocess.run(cmd, shell=True)


    except KeyboardInterrupt:
        break