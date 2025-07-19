from tkinter import *



app = Tk()
app.title("Logs - SKRR6773")


text = Text(app)
text.delete("1.0", END)
text.insert(END, open("SYNTAX", 'r', encoding='utf-8').read())
text.config(state=DISABLED)
text.pack(fill=BOTH, expand=1)


app.mainloop()