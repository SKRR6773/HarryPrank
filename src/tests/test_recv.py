from io import BytesIO
from typing import List


SPLITTER = b'</END>'

with BytesIO(b'eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>eyJoZWFkZXJzIjogeyJOYW1lIjogImEiLCAiQ29udGVudC1UeXBlIjogIlNUUiIsICJWZXJzaW9uIjogIjEuMCIsICJSZWYtSUQiOiAiMTIwMjJhMDUtYmFhNS00ZWY1LTllZjYtODkzMTBiZjdmNzE3In0sICJib2R5IjogImEifQ==</END>')as buffer:
    _buffer = b''
    segments: List[bytes] = []

    while True:
        data = buffer.read(10)


        if not data:
            break


        # print(data)

        _buffer += data



        while SPLITTER in _buffer:
            indexOf = _buffer.index(SPLITTER)
            command = _buffer[:indexOf]
            _buffer = _buffer[indexOf + len(SPLITTER): ]


            # print(command)
            segments.append(command)



    print(_buffer)
    print(segments)





