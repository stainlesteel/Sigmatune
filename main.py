import os
import tkinter as t
from tkinter import ttk
import sv_ttk
from tkinter import font
from tkinter import Tk
from tkinter import filedialog
import random
import glob
from tinytag import TinyTag
from tkinter import messagebox
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame import mixer
from pygame.mixer import music
root = t.Tk()
root.option_add('*font', 'Arial 10')
sv_ttk.set_theme('dark')
root.minsize(400, 300)
root.maxsize(600, 400)
root.title("Sigmatune")
root.resizable(True, True)

index = 0
files = []
gol = None
sigma = None
stop = None
pv = None
nv = None
tuff = None
isplay = False
def open(event=None):
    global h1
    global main
    global form
    global items

    items = filedialog.askopenfilename(
        title='Open File..',
        filetypes=(
            ('MP3 files', '*.mp3'),
            ('OGG files', '*.ogg'),
            ('WAV files', '*wav')
            )
    )
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unload()
        stop.pack_forget()
        paus.pack_forget()
        music_name.pack_forget()
    
    pygame.mixer.music.load(items)
    ui()
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)

def fopen(event=None):
    global fpath
    global sigma
    global bank
    global items
    global pv
    global nv
    global tuff
    global nt
    ext = ['mp3', 'ogg', 'wav']

    dpath = filedialog.askdirectory(title="Files won't be shown here.")
    num = 0
    for e in ext:
       pattern = os.path.join(dpath, f"*.{ext[num]}").lower()
       mpath = glob.glob(pattern)
       files.extend(mpath)
       num += 1
    try:
      items = files[0]
    except IndexError:
      messagebox.showerror("No music", "you have no rizz blud, there is no music here.")
    
    def tuf(event=None):
        global files
        global items
        random.shuffle(files)
        items = files[0]
        tklist = t.Variable(value=files)
        sigma.config(listvariable=tklist)
        pygame.mixer.music.load(items)   
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
        twe = os.path.basename(items)
        music_name.config(text=twe)


    def bank(event):
        global indice
        global index
        indice = sigma.curselection()
        index = indice[0]
        idx = index
        items = sigma.get(index)
        twe = os.path.basename(items)
        music_name.config(text=twe)
        pygame.mixer.music.load(items)   
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)    


    def pt(event=None):
        global index
        try:
         index -= 1
         items = sigma.get(index)          
         twe = os.path.basename(items)
         music_name.config(text=twe)
         pygame.mixer.music.load(items)   
         pygame.mixer.music.set_volume(0.5)
         pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
        except pygame.error:
            index = 0
            items = sigma.get(index)          
            twe = os.path.basename(items)
            music_name.config(text=twe)

    def nt(event=None): 
        global index
        try:
         index += 1
         items = sigma.get(index)          
         twe = os.path.basename(items)
         music_name.config(text=twe)
         pygame.mixer.music.load(items)   
         pygame.mixer.music.set_volume(0.5)
         pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
        except pygame.error:
            index -= 1
            items = sigma.get(index)          
            twe = os.path.basename(items)
            music_name.config(text=twe)
    
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
    fpath = files[0]
    pygame.mixer.music.load(fpath)   
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)
    ui()
    
    pv = ttk.Button(root, text="Previous Track", command=pt)
    pv.pack(pady=5)
    nv = ttk.Button(root, text="Next Track", command=nt)
    nv.pack(pady=5)
    
    tuff = ttk.Button(root, text="Shuffle", command=tuf)
    tuff.pack(pady=5)

    tklist = t.Variable(value=files)
    rizz = len(files)
    sigma = t.Listbox(root, listvariable=tklist, height=rizz, width=20)
    sigma.pack(pady=10, expand=True, fill=t.X)
    sigma.bind('<<ListboxSelect>>', bank)


def ui():
    global music_name
    global h1
    global main
    global form
    global sto
    global stop
    global paus
    global items
    global files
    global gol
    h1.pack_forget()
    main.pack_forget()
    form.pack_forget()
    filename = os.path.basename(items)
    
    music_name = ttk.Label(root, font="Arial 20")
    music_name.config(text=filename)
    music_name.pack(padx=10)
    def pause():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            paus.config(text="Play")
        else:
            pygame.mixer.music.unpause()
            paus.config(text="Pause")
            
    def stp():
        global stop, paus, music_name, vol
        pygame.mixer.music.stop()
        stop.pack_forget()
        paus.pack_forget()
        music_name.pack_forget()
        vol.pack_forget()
        if sigma:
         sigma.pack_forget()
         pv.pack_forget()
         nv.pack_forget()
         tuff.pack_forget()
        gol.pack_forget()
        
        h1.pack()
        main.pack()
        form.pack()
        pygame.mixer.music.unload()
    def volume(val):
        pygame.mixer.music.set_volume(0.5)
        vold = float(val) / 100.0
        pygame.mixer.music.set_volume(vold)
    def pos(vdl):
          gold = float(vdl)
          pygame.mixer.music.set_pos(gold)


    tag = TinyTag.get(items)
    gol = ttk.Scale(
        root,
        from_=0,
        to=tag.duration,
        orient="horizontal",
        command=pos,
        length=400
    )
    gol.set(0)
    gol.pack(pady=5)
    vol = ttk.Scale(
        root,
        from_=0,
        to=100,
        orient="horizontal",
        command=volume,
        length=200
    )
    vol.set(50)
    vol.pack(pady=10)
    
    stop = ttk.Button(root, text="Stop", command=stp)
    stop.pack(pady=10)        
    paus = ttk.Button(root, text="Pause", command=pause)
    paus.pack()
    

    root.after(100, upd)


mbar = t.Menu(root)
root.config(menu=mbar)
file = t.Menu(mbar, tearoff=False)
file.add_command(label="Open File",command=open)
file.add_command(label="Open Folder", command=fopen)
mbar.add_cascade(label="File", menu=file)


h1 = ttk.Label(root, text="🎵  Sigmatune", font="Arial 30")
h1.pack(pady=20, anchor="center")
main = ttk.Label(root, text="Hover over the menu bars (top left) to get started.")
main.pack(anchor="center")
form = ttk.Label(root, text="MP3, OGG, and WAV files are supported.")
form.pack(anchor="center")

root.bind('<Control-s>', open)
root.bind('<Command-s>', open)
root.bind('<Control-a>', fopen)
root.bind('<Command-a>', fopen)

root.mainloop()
