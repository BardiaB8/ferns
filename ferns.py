from cryptography.fernet import Fernet
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from time import sleep
from pynput.keyboard import Controller, Key, GlobalHotKeys
from pynput import mouse
import sys
try:
    #for use on High-DPI displays
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    print("...")

keyboard = Controller()
mouseController = mouse.Controller()

tk = Tk()
tk.title("Ferns")
#functions
def close():
    with open(".geometry" ,"w") as geometryFile:
        geometryFile.write(jot.winfo_geometry())
    sys.exit()
def copyToClipboard(clip):
    tk.clipboard_clear()
    tk.clipboard_append(clip)
def decryptFromClipboard():
    msg = cipher.decrypt(tk.clipboard_get().encode()).decode()
    msglbl.config(text=msg)
    pos = mouseController.position #get mouse position
    msgTop.geometry("+{0}+{1}".format(pos[0], pos[1]))
    msgTop.deiconify()
def decryptCopyAndPaste():
    #Ctrl+C, to copy the message:
    keyboard.press(Key.ctrl)
    keyboard.press("c")
    keyboard.release("c")
    keyboard.release(Key.ctrl)
    jot.after(50, decryptFromClipboard)
def loadKey():
    global cipher
    keyPath = askopenfilename(title="Select .ferns key", filetypes=[("Ferns Key File", ".ferns"), ("TXT file", ".txt")])
    with open(keyPath, 'rb') as keyfile:
        key = keyfile.read()
        cipher = Fernet(key)
    managebtn.config(text="Decrypt (from clipboard)", command=decryptFromClipboard)
    jot.attributes('-topmost', 'true') #make this window stay above all others
    try:
        with open(".geometry", "r") as geometryFile:
            jot.geometry(geometryFile.read())
    except:
        pass
    jot.deiconify()
    InputText.config(state="normal")

#Jot window functions
def Drag(Event): #drag the window to where the mouse pointer is.
    #Disable_changing_transparency() #prevent changing opacity when window is being dragged.
    jot.geometry("+{}+{}".format(Event.x_root, Event.y_root))
def Send(): #Encrypts and sends message
    msg = InputText.get().encode()
    #alt+tab to switch to other application
    keyboard.press(Key.alt)
    keyboard.press(Key.tab)
    keyboard.release(Key.alt)
    keyboard.release(Key.tab)
    sleep(1)
    copyToClipboard(cipher.encrypt(msg))
    keyboard.press(Key.ctrl)
    keyboard.press("v")
    keyboard.release("v")
    keyboard.release(Key.ctrl)
    sleep(0.1)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    #keyboard.type(cipher.encrypt(msg))

#Icons for buttons:
Send_image = PhotoImage(file="data/send.png") #send icon. from icons8.com
Close_image = PhotoImage(file="data/close.png") #close icon. from icons8.com
Drag_image = PhotoImage(file="data/drag.png") #drag icon. also from icons8.com

Label(tk, text="Please select a key.").pack(fill="x")
managebtn = Button(tk, text="Select Key", command=loadKey)
managebtn.pack(fill="x")
Button(tk, text="Quit", command=close).pack(fill="x")
#Toplevel for decrypted message
msgTop = Toplevel()
msgTop.wm_overrideredirect(True) #hide x button
msgTop.attributes('-topmost', 'true')
msgButtonsFrame = Frame(msgTop)
msgButtonsFrame.pack(fill="x")
msgDrag_btn = Button(msgButtonsFrame, image=Drag_image)
msgDrag_btn.pack(side="left")
msgDrag_btn.bind("<B1-Motion>", lambda Event: msgTop.geometry("+{}+{}".format(Event.x_root, Event.y_root)))
msglbl = Label(msgTop, font=("Vazirmatn", 12))
msglbl.pack()
Button(msgButtonsFrame, image=Close_image, command=msgTop.withdraw).pack(side="left")
Button(msgButtonsFrame, text="Copy", command=lambda: copyToClipboard(msglbl["text"])).pack(side="left")

msgTop.withdraw()

#Jot toplevel
jot = Toplevel()
jot.withdraw()
jot.wm_overrideredirect(True)
#create widgets:
InputText = Entry(jot, justify="right", width=40, font=('Vazirmatn', 12))
Send_btn = Button(jot, image=Send_image, command=Send)
Close_btn = Button(jot, image=Close_image, command=close)
Drag_btn = Button(jot, image=Drag_image)
#place widgets on screen:
Drag_btn.pack(side="left", fill="y")
InputText.pack(side="left", fill="both", expand=True)
Send_btn.pack(side="left", fill="y")
Close_btn.pack(side="left", fill="y")

Drag_btn.bind("<B1-Motion>", Drag)

#Add hotkey listener for message decryption
g = GlobalHotKeys({"<ctrl>+.":decryptCopyAndPaste})
g.start()

tk.mainloop()