from tkinter import *
from PIL import ImageTk, Image
import threading
import requests
import time
import io


app = Tk()

app.attributes("-fullscreen", True)
app.wm_attributes("-topmost", True)

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()


def closeApp():
    global app


    if app:
        app.destroy()
        app = None



def timedow():
    time.sleep(30)

    closeApp()


def dowloadImage(url: str) -> bytes:
    try:
        with requests.get(url, timeout=10)as req:
            return req.content

    except Exception as ex:
        print(ex)
        return None







image_bytes = dowloadImage("http://localhost:8000/gratisography-augmented-reality-800x525.jpg")

if image_bytes:
    with io.BytesIO(image_bytes)as image_io:
        image_io.seek(0)

        with Image.open(image_io)as image_reader:
            image_reader = image_reader.resize((screen_width, screen_height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image_reader)
            Label(app, text="Hello", width=screen_width, height=screen_height, image=photo).pack(expand=True, fill=BOTH)




threading.Thread(target=timedow, args=(), daemon=True).start()


app.bind_all("<Escape>", lambda e: closeApp())


app.mainloop()