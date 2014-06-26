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
	root_disk.withdraw()
	root_sel =Tkinter.Tk()
	root_sel.title("AUPEDACO")
	f = Frame(root_sel, width=1000, bg="blue")
	root_sel.geometry("700x700")
	f.pack_propagate(0)
	
	 
	
	
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
		lev['values'] = ['0','1','5','6','10']
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
		b.place(x=500, y=300)
		
	sel = Button(root_sel, text='Next', command=raid_creation)
	sel.pack()
	sel.place(x=400, y=300)

a = Button(root_disk, text='Create_RAID', command=create_raid)
a.pack()
a.place(x=100, y=100)

def display_raid():
	root_dis =Tkinter.Tk()
	root_dis.title("AUPEDACO")
	f = Frame(root_dis, width=1000, bg="blue")
	root_dis.geometry("700x700")
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
	level=[]
	for line in open('C:\Program Files\cmdline\output.txt','r'):
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
	
	
b = Button(root_disk, text='Display_RAID', command=display_raid)
b.pack()
b.place(x=100, y=200)

def delete_raid():
	root_sel =Tkinter.Tk()
	root_sel.title("AUPEDACO")
	f = Frame(root_sel, width=1000, bg="blue")
	root_cr.geometry("700x700")
	f.pack_propagate(0)
	
c = Button(root_disk, text='Delete_RAID', command=delete_raid)
c.pack()
c.place(x=100, y=400)


root_disk.mainloop()