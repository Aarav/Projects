import easygui as eg
import sys
import csv
import os
import pywinauto
import datetime
import re
import shlex
import Tkinter
import tkMessageBox
import glob 
import shutil
from ctypes import windll
import subprocess

import string
import time

from Tkinter import *
import ttk

root_disk =Tkinter.Tk()
root_disk.title("AUPEDACO")
f = Frame(root_disk, width=1000, bg="blue")
root_disk.geometry("700x700")
f.pack_propagate(0)


l = Label(root_disk, text="Select the RAID Type", width=50,bg="red", fg="white")
l.pack()
l.place(x=110, y=20)    
    
d= ttk.Combobox(root_disk)
d['values'] = ['Simple Volume','Raid 0','Raid 1','Raid 5','Raid 6','Raid 10']
d.bind('<<ComboboxSelected>>')
d.current(0)
d.pack()
d.place(x=200, y=40)		

l = Label(root_disk, text="Enter the size of the array", width=50,bg="red", fg="white")
l.pack()
l.place(x=110, y=80)

p = Entry(root_disk)
p.pack()
p.place(x=200, y=100) 

d= ttk.Combobox(root_disk)
d['values'] = ['MB','GB','TB']
d.bind('<<ComboboxSelected>>')
d.current(0)
d.pack()
d.place(x=400, y=100)	

l = Label(root_disk, text="Enable Read Cache", width=50, bg="red", fg="white")
l.pack()
l.place(x=110, y=160)    
d= ttk.Combobox(root_disk)
d['values'] = ['Yes','No']
d.bind('<<ComboboxSelected>>')
d.current(0)
d.pack()
d.place(x=200, y=180)

l = Label(root_disk, text="Enable Write Cache", width=50, bg="red", fg="white")
l.pack()
l.place(x=110, y=220)    
d= ttk.Combobox(root_disk)
d['values'] = ['Yes','No']
d.bind('<<ComboboxSelected>>')
d.current(0)
d.pack()
d.place(x=200, y=240)

l = Label(root_disk, text="Select Build Type", width=50, bg="red", fg="white")
l.pack()
l.place(x=110, y=280)    
d= ttk.Combobox(root_disk)
d['values'] = ['Skip','Quick','Init','Build/Verify']
d.bind('<<ComboboxSelected>>')
d.current(0)
d.pack()
d.place(x=200, y=300)




root_disk.mainloop()