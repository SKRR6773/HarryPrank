from dataclasses import dataclass
from typing import List


SPLITTER = b'</END>'

HELLOCLIENT_PORT = 6773
SERVER_PORT = 6774

EX_SERVER_NAME = "s6773code.thddns.net"
EX_SERVER_PORT = 8990


@dataclass
class CommandNamePermit:
    is_admin: bool
    command_name: str



COMMANDS: List[CommandNamePermit] = [
    CommandNamePermit(True, "GetAllClient")
]


EXIT_KEYS = [
    'exit', 'quit', 'stop'
]

CLEAR_KEYS = [
    'clear', 'cls', 'clean', 'flush'
]


IS_DEV = False

BROADCAST_INTERTIME = 10