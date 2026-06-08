from spake2 import SPAKE2_A, SPAKE2_B
import base64
from tkinter import *
from tkinter.filedialog import asksaveasfilename

tk = Tk()
tk.title("SPAKE2 Key Exchange")

def copyToClipboard(clip):
    tk.clipboard_clear()
    tk.clipboard_append(clip)
def finish(s):
    key_path = asksaveasfilename(title="Create .ferns key", filetypes=[("Ferns Key File", ".ferns"), ("TXT file", ".txt")])
    reply = base64.b64decode(tk.clipboard_get())
    key = s.finish(reply)
    fernet_key = base64.urlsafe_b64encode(key)
    with open(key_path, 'wb') as f:
        f.write(fernet_key)
def roleA():
    tk.title("SPAKE2 Role A")
    s = SPAKE2_A(password.get().encode())
    lbl.config(text="A message will been copied to your clipboard.\nPlease send it to participant B.\nThen, paste participant B's answer here.")
    msg = base64.b64encode(s.start())
    btn1.config(text="Copy your message", command = lambda: copyToClipboard(msg))
    btn2.config(text="Paste reply", command = lambda: finish(s))
def roleB():
    tk.title("SPAKE 2 Role B")
    q = SPAKE2_B(password.get().encode())
    lbl.config(text="A message will been copied to your clipboard.\nPlease send it to participant A.\nThen, paste participant A's answer here.")
    msg = base64.b64encode(q.start())
    btn1.config(text="Copy your message", command = lambda: copyToClipboard(msg))
    btn2.config(text="Paste reply", command = lambda: finish(q))

lbl = Label(tk, text="Welcome!\n Please type in the password you've agreed on.\nThen, choose a role to perform the exchange.")
password = Entry(tk)
btn1 = Button(tk, text="ROLE A", command=roleA)
btn2 = Button(tk, text="ROLE B", command=roleB)
lbl.pack()
password.pack(fill="x")
btn1.pack(fill="x")
btn2.pack(fill="x")

tk.mainloop()