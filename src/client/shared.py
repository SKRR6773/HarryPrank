from threading import Thread
from typing import List


main_task: List[Thread] = []

hand_shake = None
client = None

server_ip: str = None
is_running = True

