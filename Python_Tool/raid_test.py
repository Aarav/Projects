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

def create_raid():
    try:
        root_disk.withdraw()
        root_sel =Tkinter.Tk()
        root_sel.title("AUPEDACO")
        f = Frame(root_sel, width=1000, bg="blue")
        root_sel.geometry("700x700")
        f.pack_propagate(0)
    
        inkscape_dir=r"C:\Program Files\cmdline"
        assert os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        with open('C:\Program Files\cmdline\output.txt', 'wb') as f:
            process= subprocess.Popen(['arcconf',"getconfig","1"],stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, ''):
                sys.stdout.write(line)
                f.write(line)
        symbolList=[]
        for line in open('C:\Program Files\cmdline\output.txt','r'):
            if 'Model' in line:
                symbolList.append(line.split()[2:4])
   
        l = Label(root_sel, text="Select the drives", width=50,bg="red", fg="white")
        l.pack()
        l.place(x=110, y=20)    
         
        listbox = Listbox(root_sel , selectmode=MULTIPLE,width=50)
        for option in symbolList:
            listbox.insert(0,option)
        listbox.pack()
        listbox.place(x=110, y=40)
    except WindowsError:
        root_sel.withdraw()
        eg.msgbox("There are no Physical drives attached to the system .") 
        
        root_disk.deiconify() 	
        
def raid_creation():
    root_sel.withdraw()
    disks=listbox.curselection()
    print disks
    
    root_cr =Tkinter.Tk()
    root_cr.title("AUPEDACO")
    f = Frame(root_disk, width=1000, bg="blue")
    root_cr.geometry("700x700")
    f.pack_propagate(0)


    l = Label(root_cr, text="Select the RAID Type", width=50,bg="red", fg="white")
    l.pack()
    l.place(x=110, y=20)    

    lev= ttk.Combobox(root_cr)
    lev['values'] = ['0','1','1E','10','5','5EE','50','6','60']
    lev.bind('<<ComboboxSelected>>')
    lev.current(0)
    lev.pack()
    lev.place(x=200, y=40)		

    l = Label(root_cr, text="Enter the size of the array", width=50,bg="red", fg="white")
    l.pack()
    l.place(x=110, y=80)

    p = Entry(root_cr)
    p.pack()
    p.place(x=200, y=100) 

    d= ttk.Combobox(root_cr)
    d['values'] = ['MB']
    d.bind('<<ComboboxSelected>>')
    d.current(0)
    d.pack()
    d.place(x=400, y=100)	

    l = Label(root_cr, text="Enable Read Cache", width=50, bg="red", fg="white")
    l.pack()
    l.place(x=110, y=160)    
    d= ttk.Combobox(root_cr)
    d['values'] = ['Yes','No']
    d.bind('<<ComboboxSelected>>')
    d.current(0)
    d.pack()
    d.place(x=200, y=180)

    l = Label(root_cr, text="Enable Write Cache", width=50, bg="red", fg="white")
    l.pack()
    l.place(x=110, y=220)    
    d= ttk.Combobox(root_cr)
    d['values'] = ['Yes','No']
    d.bind('<<ComboboxSelected>>')
    d.current(0)
    d.pack()
    d.place(x=200, y=240)

    l = Label(root_cr, text="Select Build Type", width=50, bg="red", fg="white")
    l.pack()
    l.place(x=110, y=280)    
    d= ttk.Combobox(root_cr)
    d['values'] = ['Skip','Quick','Init','Build/Verify']
    d.bind('<<ComboboxSelected>>')
    d.current(0)
    d.pack()
    d.place(x=200, y=300)
    
    def creation():
        level=lev.get()
        size=p.get()
        
        print level,size
        
        inkscape_dir=r"C:\Program Files\cmdline"
        assert os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        with open('C:\Program Files\cmdline\output.txt', 'wb') as f:
            process= subprocess.Popen(['arcconf',"create","1","logicaldrive",size,level,"0","0","0","1","0","2","0","3","noprompt"],stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, ''):
                sys.stdout.write(line)
                f.write(line)
                
        eg.msgbox("Raid Created") 
        root_cr.withdraw()
        root_disk.deiconify()    
            
            
        '''inkscape_dir=r"C:\Program Files\cmdline\"
        assert os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        
        process= subprocess.Popen(['arcconf',"create","1","logicaldrive","50000","5","0","0","0","1","0","2","0","3","no prompt"],stdout=subprocess.PIPE)
        
                        
        except IOError:
            eg.msgbox("An error occured trying to read the file.") 
            root_disk.deiconify()    
        
        except ValueError:
            eg.msgbox("Non-numeric data found in the file.") 
            root_disk.deiconify()    
                        
        except ImportError:
            eg.msgbox("NO module found") 
            root_disk.deiconify()    
                            
        except EOFError:
            eg.msgbox("Why did you do an EOF on me?") 
            root_disk.deiconify()    
            
        except KeyboardInterrupt:
            eg.msgbox("Why did you do an EOF on me?") 
            root_disk.deiconify()    
        except:
            print('An error occured.Raid level cannot be created')
            root_disk.deiconify()  '''
        b= Button(root_cr, text='Create', command=creation)
        b.pack()
        b.place(x=500, y=400)
        
    sel = Button(root_sel, text='Next', command=raid_creation)
    sel.pack()
    sel.place(x=400, y=300)

    def back_create():
        root_sel.withdraw()
        root_disk.deiconify()
    back= Button(root_sel, text='Back', command=back_create)
    back.pack()
    back.place(x=40, y=300)
    
   
a = Button(root_disk, text='Create_RAID', command=create_raid)
a.pack()
a.place(x=100, y=100)

def display_raid():
    root_disk.withdraw()
    try:
        root_dis =Tkinter.Tk()
        root_dis.title("AUPEDACO")
        f = Frame(root_dis, width=1000, bg="blue")
        root_dis.geometry("700x700")
        f.pack_propagate(0)
        
        inkscape_dir=r"C:\Program Files\cmdline"
        assert os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        '''with open('C:\Program Files\cmdline\output.txt', 'wb') as f:'''
        name=[]
        level=[]
        for line in open('C:\Python27\try.txt','r'):
            if 'Logical device name ' in line:
                name.append(line.split()[4:6])
            if 'RAID level ' in line:
                level.append(line.split()[-1])
        print name,level
        
        l = Label(root_dis, text="RAID_NAME", width=50, bg="red", fg="white")
        l.pack()
        l.place(x=110, y=20)    
        listbox = Listbox(root_dis, selectmode=MULTIPLE,width=50)
        for option in name:
            listbox.insert(0,option)
        listbox.pack()
        listbox.place(x=110, y=40)
        
        l = Label(root_dis, text="RAID_LEVEL", width=50, bg="red", fg="white")
        l.pack()
        l.place(x=110, y=120)    
        
        listbox1 = Listbox(root_dis, selectmode=MULTIPLE,width=50)
        for option in level:
            listbox1.insert(0,option)
        listbox1.pack()
        listbox1.place(x=110, y=140)
        
        def back_show():
            root_dis.withdraw()
            root_disk.deiconify()
        back= Button(root_dis, text='back', command=back_show)
        back.pack()
        back.place(x=40, y=400)
        
    except IOError:
        root_dis.withdraw()
        eg.msgbox("There are no RAID LEVELS to display .") 
        root_disk.deiconify() 
b = Button(root_disk, text='Display_RAID', command=display_raid)
b.pack()
b.place(x=100, y=200)

def delete_raid():
    try:
        root_disk.withdraw()
        root_sel =Tkinter.Tk()
        root_sel.title("AUPEDACO")
        f = Frame(root_sel, width=1000, bg="blue")
        root_sel.geometry("700x700")
        f.pack_propagate(0)
        
        inkscape_dir=r"C:\Program Files\cmdline"
        assert os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        with open('C:\Program Files\cmdline\output.txt', 'wb') as f:
            process= subprocess.Popen(['arcconf',"getconfig","1","ld"],stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, ''):
                sys.stdout.write(line)
                f.write(line)
        name=[]
        
        for line in open('C:\Program Files\cmdline\output.txt','r'):
            if 'Logical device name ' in line:
                name.append(line.split()[4:6])
        
        l = Label(root_sel, text="RAID_NAME", width=50, bg="red", fg="white")
        l.pack()
        l.place(x=110, y=20)    
        listbox = Listbox(root_sel, selectmode=MULTIPLE,width=50)
        for option in name:
            listbox.insert(0,option)
        listbox.pack()
        listbox.place(x=110, y=40)
        
        def delete():
            inkscape_dir=r"C:\Program Files\cmdline"
            assert os.path.isdir(inkscape_dir)
            os.chdir(inkscape_dir)
            with open('C:\Program Files\cmdline\output.txt', 'wb') as f:
                process= subprocess.Popen(['arcconf',"delete","1","logicaldrive","0","noprompt"],stdout=subprocess.PIPE)
                for line in iter(process.stdout.readline, ''):
                    sys.stdout.write(line)
                    f.write(line)

            eg.msgbox("Raid Deleted") 
            root_sel.withdraw()
            root_disk.deiconify()
        delete1= Button(root_sel, text='Delete', command=delete)
        delete1.pack()
        delete1.place(x=500, y=40)
        def back_delete():
            root_sel.withdraw()
            root_disk.deiconify()
        back= Button(root_sel, text='Back', command=back_delete)
        back.pack()
        back.place(x=40, y=400)
    except WindowsError:
        root_sel.withdraw()
        eg.msgbox("There are no RAID Levels to Delete.") 
        root_disk.deiconify() 	 
c = Button(root_disk, text='Delete_RAID', command=delete_raid)
c.pack()
c.place(x=100, y=300)
def tutorial():
    root_disk.withdraw()
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
            
    root_di =Tkinter.Tk()
    root_di.title("AUPEDACO")
    f = Frame(root_di, width=1000, bg="blue")
    root_di.geometry("700x700")
    f.pack_propagate(0)

    def raid_0():       
        filename="C:/Python27/Raid_tutorial/raid_0.txt"  
        image_location="C:/Python27/Raid_tutorial/images/raid-0.jpg"                  
        raid0 = tutorial(0,filename,image_location)
        raid0._display_()

    c = Button(root_di, text='RAID_0', command=raid_0)
    c.pack()
    c.place(x=100, y=100)
    def raid_1():       
        filename="C:/Python27/Raid_tutorial/raid_1.txt"  
        image_location="C:/Python27/Raid_tutorial/images/raid-1.jpg"                  
        raid1 = tutorial(1,filename,image_location)
        raid1._display_()
        
    c = Button(root_di, text='RAID_1', command=raid_1)
    c.pack()
    c.place(x=100, y=150)

    def raid_5():       
        filename="C:/Python27/Raid_tutorial/raid_5.txt"  
        image_location="C:/Python27/Raid_tutorial/images/raid-5.jpg"                  
        raid5= tutorial(5,filename,image_location)
        raid5._display_()
        
    c = Button(root_di, text='RAID_5', command=raid_5)
    c.pack()
    c.place(x=100, y=200)
    def raid_6():       
        filename="C:/Python27/Raid_tutorial/raid_6.txt"  
        image_location="C:/Python27/Raid_tutorial/images/raid-6.jpg"                  
        raid5= tutorial(6,filename,image_location)
        raid5._display_()
        
    c = Button(root_di, text='RAID_6', command=raid_6)
    c.pack()
    c.place(x=100, y=250)
    def raid_10():       
        filename="C:/Python27/Raid_tutorial/raid_10.txt"  
        image_location="C:/Python27/Raid_tutorial/images/raid-10.jpg"                  
        raid10= tutorial(10,filename,image_location)
        raid10._display_()
        
    c = Button(root_di, text='RAID_10', command=raid_10)
    c.pack()
    c.place(x=100, y=300)

    def raid_50():       
        filename="C:/Python27/Raid_tutorial/raid_50.txt"  
        image_location="C:/Python27/Raid_tutorial/images/raid-50.jpg"                  
        raid50= tutorial(50,filename,image_location)
        raid50._display_()
        
    c = Button(root_di, text='RAID_50', command=raid_50)
    c.pack()
    c.place(x=100, y=350)

    def raid_60():       
        filename="C:/Python27/Raid_tutorial/raid_60.txt"  
        image_location="C:/Python27/Raid_tutorial/images/raid-60.jpg"                  
        raid60= tutorial(60,filename,image_location)
        raid60._display_()
        
    c = Button(root_di, text='RAID_60', command=raid_60)
    c.pack()
    c.place(x=100, y=400)
    
    def back():
        root_di.withdraw()
        root_disk.deiconify()
    
    c = Button(root_di, text='BACK', command=back)
    c.pack()
    c.place(x=10, y=500)
d = Button(root_disk, text='TUTORIAL', command=tutorial)
d.pack()
d.place(x=100, y=400)


root_disk.mainloop()