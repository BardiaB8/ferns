from tkinter import *
from cryptography.fernet import Fernet

tk = Tk()

def createKey(): #generates a key, then saves it to a file.
    name = nameEntry.get()
    key = Fernet.generate_key()
    with open("KEYS/{name}.ferns".format(name=name), 'wb') as kfile:
        kfile.write(key)

Label(text="""Welcome!
Please enter a name for the key,
e.g. aliceandbob.
Keys are saved in the KEYS directory.""").pack()
newkeyFrame = Frame(tk)
newkeyFrame.pack(side="top")

nameEntry = Entry(tk)
createBtn = Button(tk, text="CREATE KEY", command=createKey)

nameEntry.pack(side="left")
createBtn.pack(side="left")

tk.mainloop()