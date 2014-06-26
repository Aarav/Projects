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


class tutorial:
    
    def __init__(self,key,filename,image_location):
        #self.name = name
        self.key = key
        #self.size=size
        #self.parity=parity
        #self.drives=drives
        self.filename=filename
        self.image_location=image_location
    def _display_(self):
        print "The level specified is  %d" % self.key
        print self.filename
        for line in open(self.filename,'r'):
            if 'Device name' in line:
                pattern=re.compile("[\s]")
                line = pattern.sub('', line)
                nvalue,name = line.split(":")
            if 'level' in line:
                print 'inside level'
                pattern=re.compile("[\s]")
                line = pattern.sub('', line)
                level_value,raid_level = line.split(":")  
                print raid_level
            if 'Disk Size' in line:
                print'inside size'
                pattern=re.compile("[\s]")
                line = pattern.sub('', line)
                svalue,size = line.split(":") 
            if  "Parity"in line:
                print"inside parity"
                pattern=re.compile("[\s]")
                line = pattern.sub('', line)
                pvalue,parity= line.split(":")
                            
            if  "Drives"in line:
                print"inside parity"
                pattern=re.compile("[\s]")
                line = pattern.sub('', line)
                dvalue,drives= line.split(":")              
        root_sel =Tkinter.Toplevel()
        root_sel.title("AUPEDACO")
        f = Frame(root_sel, width=1000, bg="blue")
        root_sel.geometry("700x700")
        f.pack_propagate(0)
        from PIL import Image, ImageTk
        Tkinter.Label(root_sel, text='NAME',
                    borderwidth=3).grid(row=1,column=1,ipadx=20,ipady=20)
        Tkinter.Label(root_sel, text='RAID_LEVEL',
                    borderwidth=3 ).grid(row=1,column=2,ipadx=20,ipady=20)
        Tkinter.Label(root_sel, text='PARITY_SPACE',
                    borderwidth=3 ).grid(row=1,column=3,ipadx=20,ipady=20)
        Tkinter.Label(root_sel, text='RAID_TOTAL_SPACE',
                    borderwidth=3 ).grid(row=1,column=4,ipadx=20,ipady=20)
        Tkinter.Label(root_sel, text='NO_OF_DRIVES',
                    borderwidth=3 ).grid(row=1,column=5,ipadx=20,ipady=20)
        Tkinter.Label(root_sel, text='%s'%(name),
                    borderwidth=3 ).grid(row=2,column=1)
        Tkinter.Label(root_sel, text='%s'%(raid_level),
                    borderwidth=3 ).grid(row=2,column=2)
        Tkinter.Label(root_sel, text='%s'%(parity),
                    borderwidth=3 ).grid(row=2,column=3)
        Tkinter.Label(root_sel, text='%s'%(size),
                    borderwidth=3 ).grid(row=2,column=4)
        Tkinter.Label(root_sel, text='%s'%(drives),
                    borderwidth=3 ).grid(row=2,column=5)
        image = Image.open(self.image_location)
        photo = ImageTk.PhotoImage(image)
        label=Label(root_sel,image=photo)
        label.image = photo 
        label.pack()
        label.grid(row=3,column=1,columnspan=5,rowspan=5,padx=5, pady=5)
        
        root_sel.mainloop()
        
root_disk =Tkinter.Tk()
root_disk.title("AUPEDACO")
f = Frame(root_disk, width=1000, bg="blue")
root_disk.geometry("700x700")
f.pack_propagate(0)

def raid_0():       
    filename="C:/Python27/Raid_tutorial/raid_0.txt"  
    image_location="C:/Python27/Raid_tutorial/images/raid-0.jpg"                  
    raid0 = tutorial(0,filename,image_location)
    raid0._display_()

c = Button(root_disk, text='RAID_0', command=raid_0)
c.pack()
c.place(x=100, y=100)
def raid_1():       
    filename="C:/Python27/Raid_tutorial/raid_1.txt"  
    image_location="C:/Python27/Raid_tutorial/images/raid-1.jpg"                  
    raid1 = tutorial(1,filename,image_location)
    raid1._display_()
    
c = Button(root_disk, text='RAID_1', command=raid_1)
c.pack()
c.place(x=100, y=150)

def raid_5():       
    filename="C:/Python27/Raid_tutorial/raid_5.txt"  
    image_location="C:/Python27/Raid_tutorial/images/raid-5.jpg"                  
    raid5= tutorial(5,filename,image_location)
    raid5._display_()
    
c = Button(root_disk, text='RAID_5', command=raid_5)
c.pack()
c.place(x=100, y=200)
def raid_6():       
    filename="C:/Python27/Raid_tutorial/raid_6.txt"  
    image_location="C:/Python27/Raid_tutorial/images/raid-6.jpg"                  
    raid5= tutorial(6,filename,image_location)
    raid5._display_()
    
c = Button(root_disk, text='RAID_6', command=raid_6)
c.pack()
c.place(x=100, y=250)
def raid_10():       
    filename="C:/Python27/Raid_tutorial/raid_10.txt"  
    image_location="C:/Python27/Raid_tutorial/images/raid-10.jpg"                  
    raid10= tutorial(10,filename,image_location)
    raid10._display_()
    
c = Button(root_disk, text='RAID_10', command=raid_10)
c.pack()
c.place(x=100, y=300)

def raid_50():       
    filename="C:/Python27/Raid_tutorial/raid_50.txt"  
    image_location="C:/Python27/Raid_tutorial/images/raid-50.jpg"                  
    raid50= tutorial(50,filename,image_location)
    raid50._display_()
    
c = Button(root_disk, text='RAID_50', command=raid_50)
c.pack()
c.place(x=100, y=350)

def raid_60():       
    filename="C:/Python27/Raid_tutorial/raid_60.txt"  
    image_location="C:/Python27/Raid_tutorial/images/raid-60.jpg"                  
    raid60= tutorial(60,filename,image_location)
    raid60._display_()
    
c = Button(root_disk, text='RAID_60', command=raid_60)
c.pack()
c.place(x=100, y=400)
"This would create second object of Employee class"
#raid1 = tutorial(1,filename)
#raid1._display_()
root_disk.mainloop()