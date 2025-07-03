import psutil


for proc in psutil.process_iter(['pid', 'name']):
    # if proc.info['name'] == "Code.exe":
    #     if "VSCODE_CWD" in proc.environ():
    #         print(proc.environ()['VSCODE_CWD'])
    #     # break

    

    # if "Taskmgr.exe" in proc.info['name']:
    #     print(proc.kill())

    print(proc.name())