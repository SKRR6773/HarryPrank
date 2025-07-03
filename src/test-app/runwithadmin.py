import os
import ctypes
import subprocess


__DIR__ = os.path.dirname(__file__)

OPENPORTSH = os.path.join(__DIR__, "openport.sh")
RULE_NAME = "Allow_ALL_Inbound"
COMMANDS = [
    f"""netsh advfirewall firewall add rule name="Allow_All_Ports" dir=in action=allow protocol=TCP localport=any""",
    f"""netsh advfirewall firewall add rule name="Allow_All_Ports" dir=in action=allow protocol=UDP localport=any"""
]

if ctypes.windll.shell32.IsUserAnAdmin() == 1:
    for cmd in COMMANDS:
        subprocess.run(["cmd", "/c", cmd], shell=True)


else:
    print("Not admin")