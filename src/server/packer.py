#! 2

from dataclasses import dataclass
from env import SPLITTER
from typing import Any, Optional
from enum import Enum
import base64
import json
import re


'''
[payload data]
{
    header: {
        *Name: str
        *Content-Type: []   // for decode in other side
        *Version: [start with 1.0]
        From:               // client UUID or server(None)
        Command-Type: [
            #   -   Server Command
            @   -   Select Target
            !   -   Common Command
        ]
        Ref-ID: str
    },
    body: [any data]
}
'''

'''
base64([payload data])</END>
'''


class ContentTypes(Enum):
    JSON = "JSON"
    STR = "STR"


class CommandTypes(Enum):
    SERVER_COMMAND = "#"
    SELECT_TARGET = "@"
    COMMON_COMMAND = ">"


@dataclass
class Pack:
    name: str
    data: Any
    ref_id: Optional[str]
    command_type: Optional[CommandTypes]
    from_sender: Optional[str]



def packV1(name: str, content_type: ContentTypes, body: Any, ref_id: str = None, command_type: ContentTypes = None, from_sender: str = None):
    
    return base64.b64encode(
        json.dumps({
            "headers": {
                "Name": name,
                "Content-Type": content_type.value if content_type else None,
                "Version": "1.0",
                "Command-Type": command_type.value if command_type else None,
                "Ref-ID": ref_id,
                "From": from_sender
            },
            "body": body
        }).encode()
    ) + b"</END>"


def unPackV1(data_encoded: bytes) -> dict:
    return json.loads(base64.b64decode(data_encoded).decode())



def parsePackV1(data_encoded: bytes) -> Pack:
    try:
        data_unpacked = unPackV1(data_encoded)

        headers = data_unpacked.get("headers")
        headers['Command-Type'] = headers['Command-Type'] or CommandTypes.COMMON_COMMAND.value


        content_type: ContentTypes = ContentTypes(headers.get("Content-Type"))
        command_type: CommandTypes = CommandTypes(headers.get("Command-Type", CommandTypes.COMMON_COMMAND.value))
        from_sender = headers.get("From", None)
        data_body = data_unpacked.get("body")
        data_body_parsed = data_body    # str by default

        if content_type == ContentTypes.JSON and type(data_body_parsed) == str:
            data_body_parsed = json.loads(data_body_parsed)


        return Pack(data_unpacked.get("headers").get("Name"), data_body_parsed, data_unpacked.get("headers").get("Ref-ID"), command_type, from_sender)

    except Exception as ex:
        print(ex)
        return None



if __name__ == "__main__":
    data_packed = packV1("ssh", ContentTypes.JSON, {
        "a": "b"
    })
    print(data_packed)

    _command = data_packed.replace(SPLITTER, b'')
    # data_unpacked = unPackV1(_command)
    # print(data_unpacked)

    print(parsePackV1(_command))
