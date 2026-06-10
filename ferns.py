from cryptography.fernet import Fernet
from tkinter import *
from tkinter.ttk import *
import sv_ttk
from tkinter.messagebox import showerror
#from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfile, askdirectory
from time import sleep
from pynput.keyboard import Controller, Key, GlobalHotKeys
from pynput import mouse
import sys
import os
try:
    #for use on High-DPI displays
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    print("...")

keyboard = Controller()
mouseController = mouse.Controller()

tk = Tk()
sv_ttk.use_dark_theme()
tk.title("Ferns")

#functions
def close():
    with open(".geometry" ,"w") as geometryFile:
        geometryFile.write(jot.winfo_geometry())
    sys.exit()
def copyToClipboard(clip):
    tk.clipboard_clear()
    tk.clipboard_append(clip)
def decryptFromClipboard(clipboard):
    try:
        msg = cipher.decrypt(tk.clipboard_get().encode()).decode()
    except:
        showerror("Decryption error", "Decryption failed.\nPlease make sure you've selected the whole message.")
        return
    msglbl.config(text=msg)
    pos = mouseController.position #get mouse position
    msgTop.geometry("+{0}+{1}".format(pos[0], pos[1]))
    msgTop.deiconify()
    copyToClipboard(clipboard) #re-copy previous content
def decryptCopyAndPaste():
    try:
        clipboard = tk.clipboard_get() #preserve clipboard content
    except:
        clipboard = ""
    #Ctrl+C, to copy the message:
    keyboard.press(Key.ctrl)
    keyboard.press("c")
    keyboard.release("c")
    keyboard.release(Key.ctrl)
    jot.after(50, lambda: decryptFromClipboard(clipboard))
def encryptFile():
    filePath = askopenfilename(title="Select file to encrypt")
    if not filePath:
        return
    randomName = os.urandom(8).hex()+".fenx"
    fenxFile = asksaveasfile(mode = "wb", title="Save Ferns encrypted file", filetypes=[("Ferns Encrypted File", ".fenx")], initialfile=randomName, defaultextension=".fenx")
    if not fenxFile:
        return
    file = open(filePath, "rb")
    content = file.read()
    #encrypt filename:
    filename = os.path.basename(filePath)
    encryptedName = cipher.encrypt(filename.encode())
    #add name to file content (first four bytes represent encrypted filename location)
    header = len(encryptedName).to_bytes(4, "big")
    encryptedContent = cipher.encrypt(content)
    toWrite = header+encryptedName+encryptedContent
    fenxFile.write(toWrite)
    fenxFile.close()
    file.close()
def decryptFile():
    fenxFilepath = askopenfilename(title="Select file to decrypt")
    if not fenxFilepath:
        return
    fenxFile = open(fenxFilepath, "rb")
    name_len = int.from_bytes(fenxFile.read(4), "big")
    encryptedName = fenxFile.read(name_len)
    encryptedContent = fenxFile.read()
    name = cipher.decrypt(encryptedName).decode()
    content = cipher.decrypt(encryptedContent)
    file = asksaveasfile(mode="wb", title="Save decrypted file", initialfile=name)
    file.write(content)
    file.close()

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
    tk.iconify()
    InputText.config(state="normal")

#Jot window functions
def Resize_start(Event):
    global initial_mouse_x, initial_width
    initial_mouse_x = Event.x_root
    initial_width = jot.winfo_width()
def Resize(Event): #drag the window to where the mouse pointer is.
    Disable_changing_transparency() #prevent changing opacity when window is being resized.
    mouse_y = mouseController.position[1]
    width = Event.x_root-initial_mouse_x+initial_width
    h = jot.winfo_height()
    jot.geometry(f"{width}x{h}")
def Send(): #Encrypts and sends message
    try:
        clipboard = tk.clipboard_get() #preserve clipboard content
    except:
        clipboard = ""
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
    tk.clipboard_clear()
    tk.clipboard_append(clipboard)
    InputText.delete(0, "end")
change_transparency = True #this is used for preventing the following function from running twice
def transparency_7(Event): #make window a little opaque
    global change_transparency
    if change_transparency:
        i = 1.0
        while i >= 0.7:
            jot.attributes("-alpha", i)
            i -= 0.1
            #Sleep some time to make the transition not immediate
            sleep(0.05)
    change_transparency = False
def transparency10(Event): #make window plain
    global change_transparency
    change_transparency = True
    jot.attributes("-alpha", 1)
def Disable_changing_transparency(): #disable fading
    jot.bind("<Enter>", lambda a: a)
    jot.bind("<Leave>", lambda a: a)
def Enable_changing_transparency(): #enable fading
    jot.bind("<Enter>", transparency10)
    jot.bind("<Leave>", transparency_7)
def Drag(Event): #drag the window to where the mouse pointer is.
    Disable_changing_transparency() #prevent changing opacity when window is being dragged.
    jot.geometry("+{}+{}".format(Event.x_root, Event.y_root))

#Icons for buttons (all from icons8.com):
Send_image = PhotoImage(file="data/send.png")
Close_image = PhotoImage(file="data/close.png")
Attach_image = PhotoImage(file="data/attach.png")
Drag_image = PhotoImage(file="data/drag.png")
Copy_image = PhotoImage(file="data/copy.png")

Label(tk, text="Please select a key.").pack(fill="x")
managebtn = Button(tk, text="Select Key", command=loadKey)
managebtn.pack(fill="x")
Button(tk, text="Change Theme", command=sv_ttk.toggle_theme).pack(fill="x")
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
Button(msgButtonsFrame, image=Copy_image, command=lambda: copyToClipboard(msglbl["text"])).pack(side="left")

msgTop.withdraw()

#Jot toplevel
jot = Toplevel()
jot.withdraw()
jot.wm_overrideredirect(True)
#create widgets:
InputText = Entry(jot, justify="right", width=30, font=('Vazirmatn', 12))
Send_btn = Button(jot, image=Send_image, command=Send)
Attach_btn = Button(jot, image=Attach_image, command=encryptFile)
Close_btn = Button(jot, image=Close_image, command=close)
Drag_btn = Button(jot, image=Drag_image)
#place widgets on screen:
Drag_btn.pack(side="left", fill="y")
InputText.pack(side="left", fill="both", expand=True)
Send_btn.pack(side="left", fill="y")
Attach_btn.pack(side="left", fill="y")
Close_btn.pack(side="left", fill="y")

Drag_btn.bind("<B1-Motion>", Drag)
Drag_btn.bind("<ButtonRelease>", lambda Event: Enable_changing_transparency())
Drag_btn.bind("<Button-3>", Resize_start)
Drag_btn.bind("<B3-Motion>", Resize)
InputText.bind("<Return>", lambda Event: Send())
Attach_btn.bind("<Button-3>", lambda Event: decryptFile())
Close_btn.bind("<Button-3>", lambda Event: InputText.delete(0, "end"))
Enable_changing_transparency()

#Add hotkey listener for message decryption
g = GlobalHotKeys({"<ctrl>+.":decryptCopyAndPaste})
g.start()

tk.mainloop()
