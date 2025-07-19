# shared.py
from threading import Thread
from typing import List
# from server.Server import Server
# from server.HelloClient import HelloClient



main_tasks: List[Thread] = []
server = None
hello_client = None

is_running = True

broad_cast_intertime = 10