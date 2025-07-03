import subprocess

proc = subprocess.Popen(['cmd.exe', '/k'], shell=True, stdin=subprocess.PIPE, text=True, bufsize=1)

print("Hello CMD ")

proc.terminate()