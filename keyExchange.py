from spake2 import SPAKE2_A, SPAKE2_B
import base64
from tkinter import *
from tkinter.filedialog import asksaveasfilename
import os
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

tk = Tk()
tk.title("SPAKE2 Key Exchange")

def copyToClipboard(clip):
    tk.clipboard_clear()
    tk.clipboard_append(clip)
    btn2.config(state="normal")
def finish_A(s):
    #B's reply only contains q.start().
    key_path = asksaveasfilename(title="Create .ferns key", filetypes=[("Ferns Key File", ".ferns"), ("TXT file", ".txt")], defaultextension=".ferns")
    reply = base64.b64decode(tk.clipboard_get())
    key = s.finish(reply)
    fernet_key = base64.urlsafe_b64encode(key)
    with open(key_path, 'wb') as f:
        f.write(fernet_key)
def paste_B():
    #A's reply contains both the salt and s.start()
    reply = base64.b64decode(tk.clipboard_get())
    salt = reply[:16]
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=2,
        lanes=4,
        memory_cost=2**16
    )
    hashed_psk = kdf.derive(password.get().encode())
    q = SPAKE2_B(hashed_psk)
    msg = base64.b64encode(q.start())
    key = q.finish(reply[16:])
    key_path = asksaveasfilename(title="Create .ferns key", filetypes=[("Ferns Key File", ".ferns"), ("TXT file", ".txt")], defaultextension=".ferns")
    fernet_key = base64.urlsafe_b64encode(key)
    with open(key_path, 'wb') as f:
        f.write(fernet_key)
    btn1.config(state="normal", command = lambda: copyToClipboard(msg))

def roleA():
    password.config(state="disabled", show="*")
    tk.title("SPAKE2 Role A")
    salt = os.urandom(16)
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=2,
        lanes=4,
        memory_cost=2**16
    )
    hashed_psk = kdf.derive(password.get().encode())
    s = SPAKE2_A(hashed_psk)
    lbl.config(text="A message will been copied to your clipboard.\nPlease send it to participant B.\nThen, paste participant B's answer here.")
    msg = base64.b64encode(salt+s.start())
    btn1.config(text="Copy your message", command = lambda: copyToClipboard(msg))
    btn2.config(text="Paste reply", state="disabled", command = lambda: finish_A(s))
def roleB():
    password.config(state="disabled", show="*")
    tk.title("SPAKE2 Role B")
    lbl.config(text="You should now receive a message from participant A.\nPlease paste it here using the button below.\nThen, a message will been copied to your clipboard.\nPlease send it to participant A.")
    btn1.config(text="Copy your message", state="disabled")
    btn2.config(text="Paste reply", command=paste_B)

lbl = Label(tk, text="Welcome!\n Please type in the password you've agreed on.\nThen, choose a role to perform the exchange.")
password = Entry(tk)
btn1 = Button(tk, text="ROLE A", command=roleA)
btn2 = Button(tk, text="ROLE B", command=roleB)
lbl.pack()
password.pack(fill="x")
btn1.pack(fill="x")
btn2.pack(fill="x")

tk.mainloop()
