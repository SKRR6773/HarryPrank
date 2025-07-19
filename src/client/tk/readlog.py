from tkinter import *
from threading import Thread



def _readLog(title: str, log_content: str):
    app = Tk()
    app.title(title)


    text = Text(app)
    text.insert(END, log_content)
    text.config(state=DISABLED)
    text.pack(expand=1, fill=BOTH)

    app.mainloop()


def readLog(title: str, log_content: str):
    Thread(target=_readLog, args=(title, log_content)).start()