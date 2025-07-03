import io
from contextlib import redirect_stdout


with io.StringIO()as buffer:

    with redirect_stdout(buffer):
        print("Hello WOrld")


    buffer.seek(0)
    print(buffer.read())
