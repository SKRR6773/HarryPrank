import subprocess


proc = subprocess.Popen('cmd', stdin=subprocess.PIPE)

print("Hello CMD ")

proc.terminate()