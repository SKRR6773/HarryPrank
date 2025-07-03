from dataclasses import dataclass
from typing import List


SPLITTER = b'</END>'

HELLOCLIENT_PORT = 6773
SERVER_PORT = 6774



@dataclass
class CommandNamePermit:
    is_admin: bool
    command_name: str



COMMANDS: List[CommandNamePermit] = [
    CommandNamePermit(True, "GetAllClient")
]