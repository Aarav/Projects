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

SPI_SETSCREENSAVEACTIVE = 17
import ctypes
def StartScreenSaver(on):

	ctypes.windll.user32.SystemParametersInfoA(SPI_SETSCREENSAVEACTIVE, on, None, 0)

StartScreenSaver(0)

global folder_name 

root =Tkinter.Tk()
root.title("RAID TOOL")
f = Frame(root, width=1000, bg="blue")
root.geometry("700x700")
f.pack_propagate(0)

var = Tkinter.IntVar()

l = Label(root, text="Enter the Folder name to store default results", width=50)
l.pack()
l.place(x=110, y=20)        
dir = Entry(root)
dir.pack()
dir.place(x=200, y=40) 
folder_name=dir.get()
c = Checkbutton(root, text="Default Configuration", variable=var)
c.pack()
c.place(x=200, y=80)
print 'value is',var.get()

l = Label(root, text="Select tool", width=10)
l.pack()
l.place(x=200, y=120) 
  
Lb1 = Listbox(root)
Lb1.insert(1, "CDM")
Lb1.insert(2, "AS SSD")
Lb1.insert(3, "Disk Wriggler")
#Lb1.insert(4, "Tool_4")

Lb1.pack(fill=BOTH, expand=1)
Lb1.bind('<<ListboxSelect>>')
Lb1.place(x=200, y=140)   

def default():
    if (var.get()):
        print 'checked'
        
        global folder_name
        
        folder_name=dir.get()
        
        print "Folder name inside default function:",folder_name
        
        ###to check whether the the local drive(D) is present and CrystalDisk is not running:
        drives = []
        drive1= []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        for drive in drives:
            typeIndex = windll.kernel32.GetDriveTypeW(u"%s:\\"%drive)
            if (typeIndex == 3 or typeIndex == 4):
                drive1.append(drive)
        f = 'C:/AUPEDACO/CDM/DMStream050/samplemacro.csv'
        print "drives are",drive1
        if 'D' in drive1:
            print 'D is present'
            ####to check whether the files are already running
            if glob.glob('D:/CrystalDiskMark*' ): 
                eg.msgbox("The old files of CDM are still in the local drive. Delete the files. ")  
            elif  glob.glob('D:\AS-SSD-COPY-TEST6'):
                eg.msgbox("The old files of AS_SSD_Copy are still in the local drive. Delete the files. ")  
            elif  glob.glob('D:\AS-SSD-COMPR-TEST42'):  
                eg.msgbox("The old files of AS_SSD_Compression are still in the local drive. Delete the files. ") 
            elif  glob.glob('D:\AS-SSD-TEST42'):
                 eg.msgbox("The old files AS_SSD are still in the local drive. Delete the files. ") 
            
            else:
                if folder_name:
                    if  glob.glob('C:\\AUPEDACO\\result\\'+folder_name+''):
                        eg.msgbox("The folder name already exists. ") 
                    else:
                        print "name"
                        os.makedirs("C:\\AUPEDACO\\result\\"+folder_name+"")
                        print "Folder name before calling CDM is :",folder_name
                        root.withdraw()
                        cdm_execute()
                        #root.withdraw()
                else:
                    print "no name"
                    eg.msgbox("Enter the folder name to store the result of th test")
                
        else:
            print 'D is not present'
            eg.msgbox("Local Drive is not present")
    else:
        print 'Check_box is not clicked'
        eg.msgbox("Check default Configuration")
   
def cdm_execute():      
    global folder_name
    print "Folder name inside CDM:",folder_name
    f = open('C:/AUPEDACO/CDM/DMStream050/samplemacro.csv', 'wb')
    write1 = csv.writer(f)
    write1.writerow(['All','1','4000','2','Random','Default_test_Configuration']) 
    f.close()
    #execute()
    
    #eg.msgbox("Default Metrics will be Executed ")   
    msg = "Do you want to start the test"
    title = "Please Confirm"    
    if eg.ynbox(msg, title): 
        from pywinauto import application
        app1=application.Application()
        app1.start_('C:/AUPEDACO/CDM/CrystalDiskMark/DiskMarkX64.exe')
        
        time.sleep(1)
        app=application.Application()
        app.start_('C:/AUPEDACO/CDM/DMStream050/DiskMarkStream.exe')
        
        dlg=app.DiskMarkStream
        app.dlg.control
        dlg.TypeKeys("{ENTER}")

        dlg1=app.Open
        app.dlg1.control
        dlg1.TypeKeys('C:\ AUPEDACO\CDM\DMStream050\samplemacro.csv')
        dlg1.TypeKeys("%o")
        
              
        dlg2=app.top_window_()
        app.dlg2.control
        dlg2.TypeKeys("{ENTER}")
                    
        dlg3=app.top_window_()
        app.dlg3.control
        dlg3.TypeKeys("{ENTER}")
        
       # AS_SSD_execute()
        
        print 'Folder name before transfering the result',folder_name
        CDM_result_transfer()
        
        #sys.exit(0)  
    else: 
        sys.exit(0)    
    
def CDM_result_transfer():
    global folder_name
     
    variable = True
    time.sleep(10)
    while variable:
        if glob.glob('D:/CrystalDiskMark*'):
            time.sleep(5) 
            variable = True;
            print 'Folder open during CDM',variable
        else:                 
            variable =False;
            
            print 'Folder open during CDM',variable
    
            date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
            dt=time.strftime("%m%d")   

            from pywinauto import application
            app1=application.Application()
            dlg=app1.CrystalDiskMark
            app1.kill_()
            
            app=application.Application()
            
            dlg=app.DiskMarkStream
            app.kill_()
            
            time.sleep(10)       
            
            print 'Folder name while transfering the result',folder_name
            src_files = os.listdir('C:/AUPEDACO/CDM/DMStream050/result')
            for file_name in src_files:
                full_file_name = os.path.join('C:/AUPEDACO/CDM/DMStream050/result/',file_name)
                if (os.path.isfile(full_file_name)):
                    shutil.move(full_file_name,'C:/AUPEDACO/result/'+folder_name+'/')
            
            print'Moved file from CDM to result directory'    
         
            ###os.rename("C:\\AUPEDACO\\result\\"+folder_name+"\\"+dt+".csv", "C:\\AUPEDACO\\result\\"+folder_name+"\\Result_CDM_"+date_string+ ".csv")
            ####os.rename("C:\\AUPEDACO\\result\\"+folder_name+"\\"+dt+".txt", "C:\\AUPEDACO\\result\\"+folder_name+"\\Result_CDM_"+date_string+".txt")
            time.sleep(3)
            print'Calling AS_SSD'
            
            AS_SSD_execute()
        

def AS_SSD_execute():
    global folder_name
    print 'Folder name after calling AS SSD',folder_name
    print'AS_SSD started'   
    from pywinauto import application
    app=application.Application()
    app.start_('C:/AUPEDACO/AS_SSD_Benchmark/AS SSD Benchmark.exe')

    dlg=app.top_window_()
    app.dlg.control
    dlg.TypeKeys("{TAB 5}")
    dlg.TypeKeys("%{DOWN}")
    dlg.TypeKeys("{DOWN}")
    dlg.TypeKeys("{ENTER}")
    dlg.TypeKeys("{TAB 2}")

    dlg=app.top_window_()
    app.dlg.control
    dlg.TypeKeys("{ENTER}")

    variable = True
    time.sleep(10)
    while variable:
        if os.path.isdir('D:\AS-SSD-TEST42') == True:
            time.sleep(5) 
            variable = True;
            print 'Folder open during AS_SSD',variable
        else:
            variable =False; 
            print 'Folder name during AS SSD',folder_name
            print 'Folder open during AS_SSD',variable
            date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")

            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("%f")
            dlg.TypeKeys("{ENTER}")
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys(' C:\\AUPEDACO\\result\\'+folder_name+'\\Result_AS_SSD_MB_'+date_string+'.png',with_spaces=True)
            dlg.TypeKeys("{ENTER}")
            
            
            dlg=app['AS SSD Benchmark 1.7.4739.38088']
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("%e")
            dlg.TypeKeys("{ENTER}")

            def Notepad(type):
                app2=application.Application()
                app2.start_('Notepad.exe')

                fine = datetime.date.today()
                print fine
                dlg=app2.top_window_()
                app2.dlg.control

                dlg.TypeKeys("^v")
                dlg.TypeKeys("^s")

                dlg=app2.top_window_()
                app2.dlg.control
                dlg.TypeKeys(' C:\\AUPEDACO\\result\\'+folder_name+'\\'+ type + date_string +'.txt',with_spaces=True)
                dlg.TypeKeys("{ENTER}")
                                      
                dlg=app2.top_window_()
                app2.dlg.control
                dlg.TypeKeys("%{F4}")
            
            ssd_type='Result_AS_SSD_MB_'
            Notepad(ssd_type)
            
            from pywinauto import application
            app=application.Application()
                    
            dlg=app['AS SSD Benchmark 1.7.4739.38088']
            #dlg=app.getitem_('AS SSD Benchmark')
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("%v")
            dlg.TypeKeys("{DOWN}")
            dlg.TypeKeys("{ENTER}")
            
            dlg.TypeKeys("%f")
            dlg.TypeKeys("{ENTER}")
                              
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys(' C:\\AUPEDACO\\result\\'+folder_name+'\\Result_AS_SSD_IOPS_'+ date_string + '.png',with_spaces=True)
            dlg.TypeKeys("{ENTER}")
            
            
            dlg=app['AS SSD Benchmark 1.7.4739.38088']
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("%e")
            dlg.TypeKeys("{ENTER}")
            
            iops_type='Result_AS_SSD_IOPS_'
            Notepad(iops_type)
            
            today = datetime.datetime.today()
            from pywinauto import application
            app=application.Application()
            dlg=app['AS SSD Benchmark 1.7.4739.38088']
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("%t")
            dlg.TypeKeys("{ENTER}")
            dlg3=app.top_window_()
            app.dlg3.control
            dlg3.TypeKeys("{ENTER}")
            variable = True
            
            time.sleep(10)
            while variable:
                #if glob.glob(m.group(1)+':/AS-SSD-COPY-TEST6'):
                if os.path.isdir('D:\AS-SSD-COPY-TEST6') == True:
                    time.sleep(5) 
                    variable = True;
                    print 'Folder open during AS_SSD_COPY:',variable
                else:
                             
                    variable =False;
                    print 'Folder open during AS_SSD_COPY:',variable        
                    date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
                           
                    dlg=app.top_window_()
                    app.dlg.control
                    dlg.TypeKeys("%f")
                    dlg.TypeKeys("{ENTER}")
                    
                    dlg=app.top_window_()
                    app.dlg.control
                    dlg.TypeKeys(' C:\\AUPEDACO\\result\\'+folder_name+'\\Result_AS_SSD_CopyBench_' + date_string +'.png',with_spaces=True)
                    dlg.TypeKeys("{ENTER}")
                    
                    
                    dlg=app['AS SSD Benchmark 1.7.4739.38088']
                    dlg=app.top_window_()
                    app.dlg.control
                    dlg.TypeKeys("%e")
                    dlg.TypeKeys("{ENTER}")
                    
                    copy_type='Result_AS_SSD_CopyBench_'
                    
                    app.kill_()
                    Notepad(copy_type)
            
                            
            from pywinauto import application
           
            app=application.Application()
            app.start_('C:/AUPEDACO/AS_SSD_Benchmark/AS SSD Benchmark.exe')
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{TAB 5}")
            dlg.TypeKeys("%{DOWN}")
            dlg.TypeKeys("{DOWN}")
            dlg.TypeKeys("{ENTER}")
            dlg.TypeKeys("%t")
            dlg.TypeKeys("{DOWN}")
            dlg.TypeKeys("{ENTER}")
            dlg3=app.top_window_()
            app.dlg3.control
            dlg3.TypeKeys("{ENTER}")
            variable = True

            time.sleep(10)
            while variable:
                #if glob.glob(m.group(1)+':/AS-SSD-COMPR-TEST42'):
                if os.path.isdir('D:\AS-SSD-COMPR-TEST42') == True:
                    time.sleep(5) 
                    variable = True;
                    print 'Folder open during AS_SSD_COMPR',variable
                else:
                    variable =False;  
                    print 'Folder open during AS_SSD_COMPR',variable
                    date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
                                                
                    dlg=app.top_window_()
                    app.dlg.control
                    dlg.TypeKeys("%f")
                    dlg.TypeKeys("{ENTER}")
                    
                    dlg=app.top_window_()
                    app.dlg.control
                    dlg.TypeKeys(' C:\\AUPEDACO\\result\\'+folder_name+'\\Result_AS_SSD_CompressionBench_' + date_string +'.png',with_spaces=True)
                    dlg.TypeKeys("{ENTER}")
                    
            app=application.Application()
            dlg=app['AS SSD Benchmark 1.7.4739.38088']
            dlg=app.top_window_()
            app.kill_()
            
            print 'Folder Closed',variable
            print 'Folder name while exiting the AS SSD',folder_name
            
            Disk_wriggler_default()
            #eg.msgbox("Default Metrics Executed and results are captured") 
            #root.deiconify()

def Disk_wriggler_default():
    global folder_name
   
    date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
    
    print 'Folder name while entering the Disk_Wriggler',folder_name
    inkscape_dir=r"C:\AUPEDACO\Disk_Wriggler\diskWriggler-1.0.1.win32"
    assert os.path.isdir(inkscape_dir)
    os.chdir(inkscape_dir)
    folder_direct='D:\\Disk_Wriggler\\'+date_string+'D'
    print folder_direct
    os.makedirs(folder_direct)
         
    tkMessageBox.showinfo("Disk Wriggler","Disk Wriggler will be Running .After Clicking OK do not press any key ")        

    with open('C:/AUPEDACO/result/'+folder_name+'/Result_Disk_Wriggler_Direct_IO_'+date_string +'.txt', 'wb') as f:
  
        process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n","4000","-o",folder_direct,'-D'],stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            f.write(line)
        shutil.rmtree(folder_direct) 
        
    with open('C:/AUPEDACO/result/'+folder_name+'/Result_Disk_Wriggler_Cached_IO_'+date_string +'.txt', 'wb') as f:
        process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n","4000","-o",folder_direct],stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            f.write(line)
        shutil.rmtree('D:\Disk_Wriggler') 
        
        print 'Folder name while exiting the Disk_Wriggler',folder_name
        eg.msgbox("Default metrics are executed and results are captured") 
        sys.exit(0)
            
b = Button(root, text='Start_Default_test', command=default)
b.pack(anchor = "e", padx=20,pady = 20)


def tools():

    hi =Lb1.get(ACTIVE) 
    print hi
    if ( hi == 'CDM'):
        root.withdraw()
        CDM()
    elif( hi == 'AS SSD'):
        root.withdraw()
        AS_SSD()
    elif ( hi == 'Disk Wriggler'):
        root.withdraw()
        Disk_Wriggler()
    else:
       eg.msgbox("Make a selection from the tools listed")  
def CDM():
    
    def execute():
        root_CDM.withdraw()
        msg = "Do you want to start the test"
        title = "Please Confirm"    
        if eg.ynbox(msg, title): 
            from pywinauto import application
            app1=application.Application()
            app1.start_('C:/AUPEDACO/CDM/CrystalDiskMark/DiskMarkX64.exe')
            
            app=application.Application()
            app.start_('C:/AUPEDACO/CDM/DMStream050/DiskMarkStream.exe')
            
            dlg=app.DiskMarkStream
            app.dlg.control
            dlg.TypeKeys("{ENTER}")

            dlg1=app.Open
            app.dlg1.control
            
            dlg1.TypeKeys('C:\ AUPEDACO\CDM\DMStream050\samplemacro.csv')
            dlg1.TypeKeys("%o")
            
                  
            dlg2=app.top_window_()
            app.dlg2.control
            dlg2.TypeKeys("{ENTER}")
                        
            dlg3=app.top_window_()
            app.dlg3.control
            dlg3.TypeKeys("{ENTER}")
                    
            CDM_result_transfer_2()
            sys.exit(0)  
            
        else: 
            sys.exit(0)    
           
        
         
    root_CDM =Tk()
    root_CDM.title("CDM:")
        
    driveTypes = ['DRIVE_UNKNOWN', 'DRIVE_NO_ROOT_DIR', 'DRIVE_REMOVABLE', 'DRIVE_FIXED', 'DRIVE_REMOTE', 'DRIVE_CDROM', 'DRIVE_RAMDISK']
    drives = []
    drive1= []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    for drive in drives:
        typeIndex = windll.kernel32.GetDriveTypeW(u"%s:\\"%drive)
        if (typeIndex == 3 or typeIndex == 4):
            drive1.append(drive)


    f = Frame(root_CDM, width=1000, bg="blue")
    root_CDM.geometry("700x700")
    f.pack_propagate(0)
    
    l = Label(root_CDM, text="Default Configuration", width=50, bg="blue", fg="white")
    l.pack()
    l.place(x=100 , y=20)
    
    l = Label(root_CDM, text="Test Drive", width=10, bg="red", fg="white")
    l.pack()
    l.place(x=200 , y=40)
    
    n = ttk.Combobox(root_CDM)
    n['values'] = [drive1]
    n.current(0)
    n.bind('<<ComboboxSelected>>')
    n.pack()
    n.place(x=200,y=60)
    n.event_generate('<Button-1>')
    def default_test():
        print 'Inside default'
        lt='All'
        tr='5'
        fs='4000'
        tdr=n.current()
        tdr1=tdr +1 
        tda='0x00'
        f = open('C:/AUPEDACO/CDM/DMStream050/samplemacro.csv', 'wb')
        write1 = csv.writer(f)
        write1.writerow([lt,tr,fs,tdr1,tda]) 
        f.close()
        execute()
        #eg.msgbox("Default Metrics will be Executed ")    
    b = Button(root_CDM, text='Start Default_test', command=default_test)
    b.pack()   
    b.place(x=500,y=60) 
   
    l = Label(root_CDM, text="Configure the Parameters", width=50, bg="blue", fg="white")
    l.pack()
    l.place(x=100 , y=100)     
                           
    l = Label(root_CDM, text="Load Type", width=10, bg="red", fg="white")
    l.pack()
    l.place(x=200, y=140)
    c = ttk.Combobox(root_CDM)
    c['values'] = ['All','Seq','512','4k','4KQD32']
    c.state(['readonly'])
    c.bind('<<ComboboxSelected>>')
    c.current(0)
    c.pack()
    c.place(x=200, y=160)

    l = Label(root_CDM, text="Test Runs", width=10, bg="red", fg="white")
    l.pack()
    l.place(x=200, y=200)    
    d= ttk.Combobox(root_CDM)
    d['values'] = ['1','2','3','4','5','6','7','8','9']
    d.bind('<<ComboboxSelected>>')
    d.current(0)
    d.pack()
    d.place(x=200, y=220)
    l = Label(root_CDM, text="File Size", width=10, bg="red", fg="white")
    l.pack()
    l.place(x=200, y=260)
    e = ttk.Combobox(root_CDM)
    e['values'] = ['50MB','100MB','500MB','1000MB','2000MB','4000MB']
    e.current(0)
    e.bind('<<ComboboxSelected>>')
    e.pack()
    e.place(x=200, y=280)
    l = Label(root_CDM, text="Test Drive", width=10, bg="red", fg="white")
    l.pack()
    l.place(x=200, y=320)
    n = ttk.Combobox(root_CDM)
    n['values'] = [drive1]
    n.current(0)
    n.bind('<<ComboboxSelected>>')
    n.pack()
    n.place(x=200, y=340)

    l = Label(root_CDM, text="Test Data", width=10, bg="red", fg="white")
    l.pack()
    l.place(x=200, y=380)
    g = ttk.Combobox(root_CDM)
    g['values'] = ['Random','0fill','1fill','0x00']
    g.current(0)
    g.bind('<<ComboboxSelected>>')
    g.pack()
    g.place(x=200, y=400)
    
    def CDM_result_transfer_2():     
    
        variable = True
        time.sleep(10)
        sim = n.get()
        m = re.search(r"\'([A-Za-z0-9_]+)\'", sim)
        while variable:
                 	
            if glob.glob(m.group(1)+':/CrystalDiskMark*'):
                print m.group(1)
                time.sleep(5) 
                print 'Folder open during CDM',variable
                variable = True
            else:                 
                variable =False;
               			    			
                print 'Folder open during CDM',variable
                
                from pywinauto import application
                app1=application.Application()
                dlg=app1.CrystalDiskMark
                app1.kill_()
                
                app=application.Application()
                
                dlg=app.DiskMarkStream
                app.kill_()
                
                time.sleep(10)    
                date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
                dt=time.strftime("%m%d")
				
                src_files = os.listdir('C:/AUPEDACO/CDM/DMStream050/result')
                for file_name in src_files:
                    full_file_name = os.path.join('C:/AUPEDACO/CDM/DMStream050/result/',file_name)
                    if (os.path.isfile(full_file_name)):
                         shutil.move(full_file_name,'C:/AUPEDACO/CDM/result')
                
                print'Moved file from CDM to result directory'    
				
                os.rename("C:\\AUPEDACO\\CDM\\result\\"+dt+".csv", "C:\\AUPEDACO\\CDM\\result\\Result_CDM_"+date_string+".csv")
                os.rename("C:\\AUPEDACO\\CDM\\result\\"+dt+".txt", "C:\\AUPEDACO\\CDM\\result\\Result_CDM_"+date_string+".txt")

                eg.msgbox("Crystal Disk Mark is performed and  Results are Stored ")
                root.deiconify()
                
    def customized_test():
        c.event_generate('<Button-1>')
        lt=c.get()
        tr=d.get()
        fs=e.get()
        tdr=n.current()
        tdr1=tdr +1 
        tda=g.get()
        f = open('C:/AUPEDACO/CDM/DMStream050/samplemacro.csv', 'wb')
        write1 = csv.writer(f)
        list1=[lt , tr, fs, tdr1, tda ]
        print list1

        write1.writerow([lt,tr,fs,tdr1,tda]) 
        f.close()
        execute()
    b = Button(root_CDM, text='Start Customized_test', command=customized_test)
    b.pack()     
    b.place(x=500,y=350)
      
    l = Label(root_CDM, text="Create Profile", width=50, bg="blue", fg="white")
    l.pack()
    l.place(x=100 , y=440)     
                           
    l = Label(root_CDM, text="Profile Name", width=10, bg="red", fg="white")
    l.pack()
    l.place(x=200, y=460)        
    
    p = Entry(root_CDM)
    p.pack()
    p.place(x=200, y=480) 
    
    def create_profile():
        c.event_generate('<Button-1>')
        lt=c.get()
        tr=d.get()
        fs=e.get()
        tdr=n.current()
        tdr1=tdr +1 
        tda=g.get()
        st=p.get()
        print st
        final = lt + " "+str(tr)+" "+ str(fs)+ " "+ str(tdr1) + " " + tda
                
        print final
        rt=[final]
        print rt
        
        thefile =open("C:/AUPEDACO/CDM/DMStream050/profiles","a")
        thefile.write("\nPROFILE NAME: %s `\n" % st)
        print>>thefile, rt
        
        thefile.write("\nPROFILE_END:\n" )
        eg.msgbox("Created PROFILE:")
        execute
               
        #print options3
    x = Button(root_CDM,text='Create_profile', command=create_profile)
    x.pack() 
    x.place(x=500,y=470)


    l = Label(root_CDM, text="Select from Created Profiles", width=50, bg="blue", fg="white")
    l.pack()
    l.place(x=100 , y=520) 
    def created_profiles():
        fh= open("C:/AUPEDACO/CDM/DMStream050/profiles","r")
        data=fh.read()
        pattern=re.compile(r'PROFILE \s*(.*?)\s*PROFILE_END:', re.DOTALL)
        matches=pattern.findall(data)
        print("the matches are ",matches)
        
        question="Select the profile from the list" 
        title = "PROFILES LIST"
        options=eg.choicebox(question,title,matches)
        #print options
        options1=options.split("[")[1]
        options2=options1[:-1]
        options3=shlex.split(options2)
        #print options3
       
        rep=eg.enterbox("Enter the count of repeat:") 
             
                     
        f = open('C:/AUPEDACO/CDM/DMStream050/samplemacro.csv', 'wb')
        w = csv.writer(f, delimiter = ',')
        count = 0
        while (count < int(rep)):
            w.writerows([x.split(' ') for x in options3])
            count = count + 1
        f.close()
        execute()
    y = Button(root_CDM,text='Created_profiles', command=created_profiles)
    y.pack() 
    y.place(x=500,y=550)
    
    def back3():
        root_CDM.withdraw()
        root.deiconify()
  
    b3=Button(root_CDM, text='back', command=back3)
    b3.pack()
    b3.place(x=60, y=680)
    
def AS_SSD():    

    root_AS=Tk()
    root_AS.title("SSD Benchmark")
    f = Frame(root_AS, width=1000, bg="blue")
    root_AS.geometry("600x600")
    f.pack_propagate(0)
    driveTypes = ['DRIVE_UNKNOWN', 'DRIVE_NO_ROOT_DIR', 'DRIVE_REMOVABLE', 'DRIVE_FIXED', 'DRIVE_REMOTE', 'DRIVE_CDROM', 'DRIVE_RAMDISK']
    drives = []
    drive1= []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    for drive in drives:
        typeIndex = windll.kernel32.GetDriveTypeW(u"%s:\\"%drive)
        if (typeIndex == 3 ):
            drive1.append(drive)
            
    n = ttk.Combobox(root_AS)
    n['values'] = [drive1]
    n.current(0)
    n.bind('<<ComboboxSelected>>')
    n.pack()

    l = Label(root_AS, text="Load Type", width=10, bg="red", fg="white")
    l.pack()
    t = ttk.Combobox(root_AS)
    t['values'] = ['All','Seq','4K','4k-64Thrd','Acc.time']
    t.state(['readonly'])
    t.bind('<<ComboboxSelected>>')
    t.current(0)
    t.pack()

    def dropdown0():
    
        root_AS.destroy()
        from pywinauto import application
        app=application.Application()
        app.start_('C:/AUPEDACO/AS_SSD_Benchmark/AS SSD Benchmark.exe')
        
        if n.current() == 1:
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{TAB 5}")
            dlg.TypeKeys("%{DOWN}")
            dlg.TypeKeys("{DOWN}")
            dlg.TypeKeys("{ENTER}")
            dlg.TypeKeys("{TAB 2}")
            
        elif n.current() == 2: 
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{TAB 5}")
            dlg.TypeKeys("%{DOWN}")
            dlg.TypeKeys("{DOWN 2}")
            dlg.TypeKeys("{ENTER}")
            dlg.TypeKeys("{TAB 2}")
            
        if t.current() == 0:
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{ENTER}")
        elif t.current() == 1:   
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")

            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")

            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
                
            dlg.TypeKeys("{TAB 3}")
            dlg.TypeKeys("{ENTER}")
        elif t.current() == 2:  
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")

            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
            
            dlg.TypeKeys("{TAB}")       
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
                
            dlg.TypeKeys("{TAB 3}")
            dlg.TypeKeys("{ENTER}")
        elif t.current() == 3:
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")

            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
            
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
                
            dlg.TypeKeys("{TAB 4}")
            dlg.TypeKeys("{ENTER}")
        
        elif t.current() == 4:
            dlg=app.top_window_()
            app.dlg.control
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
            
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
            
            dlg.TypeKeys("{TAB}")
            dlg.TypeKeys("{SPACE}")
                
            dlg.TypeKeys("{TAB 3}")
            dlg.TypeKeys("{ENTER}")
          
            
                       
            
            
        
        variable = True
        time.sleep(10)
        sim = n.get()
        m = re.search(r"\'([A-Za-z0-9_]+)\'", sim)
        while variable:
                 	
            if glob.glob(m.group(1)+':/AS-SSD-TEST42'):
		    #if os.path.isdir('C:\AS-SSD-TEST42') == True:
                time.sleep(5) 
                variable = True;
                print 'Folder open',variable
            else:
                variable =False; 
                
                date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
                #from PIL import ImageGrab, Image
                #import win32gui
                #thumbnailsize = 400, 900
                #hwnd = win32gui.FindWindow(0, "AS SSD Benchmark 1.7.4739.38088") 
                #win32gui.SetForegroundWindow(hwnd)
                #bbox = win32gui.GetWindowRect(hwnd)
                #img = ImageGrab.grab(bbox)
                #img.thumbnail(thumbnailsize, Image.ANTIALIAS)
                #img.save('C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_MB_'+ date_string + '.png')
                
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys("%f")
                dlg.TypeKeys("{ENTER}")
                
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys(' C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_MB_' + date_string +'.png',with_spaces=True)
                dlg.TypeKeys("{ENTER}")
                
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys("%e")
                dlg.TypeKeys("{ENTER}")
                
                                                                  
                
                from pywinauto import application
                app=application.Application()
                app.start_('Notepad.exe')

                fine = datetime.date.today()
                print fine
                dlg=app.top_window_()
                app.dlg.control

                dlg.TypeKeys("^v")
                dlg.TypeKeys("^s")

                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys(' C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_MB_' + date_string +'.txt',with_spaces=True)
                dlg.TypeKeys("{ENTER}")
                                      
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys("%{F4}")
                
                app=application.Application()
                dlg=app['AS SSD Benchmark 1.7.4739.38088']
                dlg=app.top_window_()
                app.kill_()
                
                print 'Folder Closed',variable
                
                eg.msgbox("AS SSD Benchmark test is completed and results are captured") 
                root.deiconify()
    a = Button(root_AS, text='SSD Benchmark', command=dropdown0)
    #a.pack(anchor = "e")
    #a.pack()
    a.place(x=10, y=100)
        
    def dropdown():
        root_AS.destroy()
        from pywinauto import application
        app=application.Application()
        app.start_('C:/AUPEDACO/AS_SSD_Benchmark/AS SSD Benchmark.exe')
        dlg=app.top_window_()
        app.dlg.control
        dlg.TypeKeys("%t")
        dlg.TypeKeys("{DOWN}")
        dlg.TypeKeys("{ENTER}")
        dlg3=app.top_window_()
        app.dlg3.control
        dlg3.TypeKeys("{ENTER}")
        variable = True
        sim = n.get()
        m = re.search(r"\'([A-Za-z0-9_]+)\'", sim)
        time.sleep(10)
        while variable:
            if glob.glob(m.group(1)+':/AS-SSD-COMPR-TEST42'):
            #if os.path.isdir('C:\AS-SSD-COMPR-TEST42') == True:
                time.sleep(5) 
                variable = True;
                print 'Folder open',variable
            else:
                variable =False;  
                
                date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
                
                #thumbnailsize = 400, 400
                #hwnd = win32gui.FindWindow(0, "AS SSD Benchmark 1.7.4739.38088") 
                #win32gui.SetForegroundWindow(hwnd)
                #bbox = win32gui.GetWindowRect(hwnd)
                #img = ImageGrab.grab(bbox)
                #img.thumbnail(thumbnailsize, Image.ANTIALIAS)
                #img.save('C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_CompressionBench_'+ date_string + '.png')
                
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys("%f")
                dlg.TypeKeys("{ENTER}")
                
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys('C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_CompressionBench_' + date_string +'.png',with_spaces=True)
                dlg.TypeKeys("{ENTER}")
                                               
                print 'Folder Closed',variable
                
                app=application.Application()
                dlg=app['AS SSD Benchmark 1.7.4739.38088']
                dlg=app.top_window_()
                app.kill_()
                
                
                eg.msgbox("AS SSD Compression Benchmark test is completed and results are captured") 
                root.deiconify()
    b= Button(root_AS, text='Compression-BenchMark', command=dropdown)
    b.pack()
    b.place(x=200, y=100)
    #b.pack()
    

    def dropdown1():
        root_AS.destroy()
        from pywinauto import application
        app=application.Application()
        app.start_('C:/AUPEDACO/AS_SSD_Benchmark/AS SSD Benchmark.exe')
        today = datetime.datetime.today()
        dlg=app.top_window_()
        app.dlg.control
        dlg.TypeKeys("%t")
        dlg.TypeKeys("{ENTER}")
        dlg3=app.top_window_()
        app.dlg3.control
        dlg3.TypeKeys("{ENTER}")
        variable = True
        
        sim = n.get()
        m = re.search(r"\'([A-Za-z0-9_]+)\'", sim)
        time.sleep(10)
        while variable:
            if glob.glob(m.group(1)+':/AS-SSD-COPY-TEST6'):
            #if os.path.isdir('C:\AS-SSD-COPY-TEST6') == True:
                time.sleep(5) 
                variable = True;
                print 'Folder open',variable
            else:
                         
                variable =False;
                        
                date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
                #from PIL import ImageGrab, Image
                #import win32gui
                #thumbnailsize = 400, 900
                #hwnd = win32gui.FindWindow(0, "AS SSD Benchmark 1.7.4739.38088") 
                #win32gui.SetForegroundWindow(hwnd)
                #bbox = win32gui.GetWindowRect(hwnd)
                #img = ImageGrab.grab(bbox)
                #img.thumbnail(thumbnailsize, Image.ANTIALIAS)
                #img.save('C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_CopyBench_'+ date_string + '.png')
        
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys("%f")
                dlg.TypeKeys("{ENTER}")
                
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys('C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_CopyBench_' + date_string +'.png',with_spaces=True)
                dlg.TypeKeys("{ENTER}")
                
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys("%e")
                dlg.TypeKeys("{ENTER}")
                                                  
                                  
                from pywinauto import application
                app=application.Application()
                app.start_('Notepad.exe')

                fine = datetime.date.today()
                print fine
                dlg=app.top_window_()
                app.dlg.control

                dlg.TypeKeys("^v")
                dlg.TypeKeys("^s")

                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys('C:\\AUPEDACO\\AS_SSD_Benchmark\\result\\Result_AS_SSD_CopyBench_' + date_string +'.txt',with_spaces=True)
                dlg.TypeKeys("{ENTER}")
                
                         
                dlg=app.top_window_()
                app.dlg.control
                dlg.TypeKeys("%{F4}")
                
                app=application.Application()
                dlg=app['AS SSD Benchmark 1.7.4739.38088']
                dlg=app.top_window_()
                app.kill_()
                
                print 'Folder Closed',variable
                
                eg.msgbox("AS SSD Copy Benchmark test is completed and results are captured") 
                root.deiconify()
    c = Button(root_AS, text='Copy-BenchMark', command=dropdown1)
    c.pack()
    c.place(x=400, y=100)
    
    def back2():
        root_AS.withdraw()
        root.deiconify()
  
    b2=Button(root_AS, text='back', command=back2)
    b2.pack()
    b2.place(x=60, y=500)
    
    
def Disk_Wriggler():

    root_disk =Tkinter.Tk()
    root_disk.title("Disk Wriggler")
    f = Frame(root_disk, width=1000, bg="blue")
    root_disk.geometry("700x700")
    f.pack_propagate(0)

    drives = []
    drive1= []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    for drive in drives:
        typeIndex = windll.kernel32.GetDriveTypeW(u"%s:\\"%drive)
        if (typeIndex == 3 or typeIndex == 4):
            drive1.append(drive)

          
    l = Label(root_disk, text="Select the Drive ", width=50,bg="red", fg="white")
    l.pack()
    l.place(x=110, y=20)        
            
    n = ttk.Combobox(root_disk)
    n['values'] = [drive1]
    n.current(0)
    n.bind('<<ComboboxSelected>>')
    n.pack()
    n.place(x=200,y=40)


    l = Label(root_disk, text="Enter the number of frames ", width=50,bg="red", fg="white")
    l.pack()
    l.place(x=110, y=80)

    p = Entry(root_disk)
    p.pack()
    p.place(x=200, y=100) 

    l = Label(root_disk, text="Check the IO Type ", width=50,bg="red", fg="white")
    l.pack()
    l.place(x=110, y=140)

    Lib1 = Listbox(root_disk)
    Lib1.insert(1, "Direct_IO")
    Lib1.insert(2, "Asyncronous_IO")
    Lib1.insert(3, "Synchronous_IO")
    Lib1.insert(4, "DirectIO_READ")
    Lib1.insert(5, "Cached_IO")


    Lib1.pack(fill=BOTH, expand=1)
    Lib1.bind('<<ListboxSelect>>')
    Lib1.place(x=200, y=160) 


    l = Label(root_disk, text="Start Default test", width=50,bg="red", fg="white")
    l.pack()
    l.place(x=110, y=400)


    def test():
        date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
        frames=p.get()
        sim = n.get()
        print 'The answer is :',sim
        m = re.search(r"\'([A-Za-z0-9_]+)\'", sim)
        r=m.group(1)
        print 'The value is :',r
        
        
      

        if frames:
                   
            inkscape_dir=r"C:\AUPEDACO\Disk_Wriggler\diskWriggler-1.0.1.win32"
            assert os.path.isdir(inkscape_dir)
            os.chdir(inkscape_dir)
            
            iotype =Lib1.get(ACTIVE) 
            
            if (iotype == 'Direct_IO'):
                folder_direct=r+':\\Disk_Wriggler\\'+date_string+'Direct_IO'
                os.makedirs(folder_direct)          
                with open('C:/AUPEDACO/Disk_Wriggler/result/Result_Disk_Wriggler_Direct_IO_'+date_string +'.txt', 'wb') as f:
              
                    process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n",frames,"-o",folder_direct,'-D'],stdout=subprocess.PIPE)
                    for line in iter(process.stdout.readline, ''):
                        sys.stdout.write(line)
                        f.write(line)
                    shutil.rmtree(folder_direct)
                    root_disk.destroy()  
                   
                    eg.msgbox("Disk Wriggler Direct IO test is completed and results are captured") 
                    root.deiconify()    
                
            elif (iotype == 'Asyncronous_IO'):
                folder_direct=r+':\\Disk_Wriggler\\'+date_string+'Async_IO'
                os.makedirs(folder_direct)
                with open('C:/AUPEDACO/Disk_Wriggler/result/Result_Disk_Wriggler_Asyncronous_IO_'+date_string +'.txt', 'wb') as f:
              
                    process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n",frames,"-o",folder_direct,'-A'],stdout=subprocess.PIPE)
                    for line in iter(process.stdout.readline, ''):
                        sys.stdout.write(line)
                    shutil.rmtree(folder_direct)
                    root_disk.destroy()  
                    eg.msgbox("Disk Wriggler Async IO test is completed and results are captured") 
                    root.deiconify()        
                        
            elif (iotype == 'Synchronous_IO'):
                folder_direct=r+':\\Disk_Wriggler\\'+date_string+'Sync_IO'
                os.makedirs(folder_direct)
                with open('C:/AUPEDACO/Disk_Wriggler/result/Result_Disk_Wriggler_Synchronous_IO_'+date_string +'.txt', 'wb') as f:
              
                    process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n",frames,"-o",folder_direct,'-S'],stdout=subprocess.PIPE)
                    for line in iter(process.stdout.readline, ''):
                        sys.stdout.write(line)
                        f.write(line)
                    shutil.rmtree(folder_direct)
                    root_disk.destroy()
                    eg.msgbox("Disk Wriggler Sync IO test is completed and results are captured") 
                    root.deiconify() 
                    
            elif (iotype == 'DirectIO_READ'):
                folder_direct=r+':\\Disk_Wriggler\\'+date_string+'Direct_Read'
                os.makedirs(folder_direct)
                with open('C:/AUPEDACO/Disk_Wriggler/result/Result_Disk_Wriggler_Direct_READ_IO_'+date_string +'.txt', 'wb') as f:
              
                    process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n",frames,"-o",folder_direct,'-DR'],stdout=subprocess.PIPE)
                    for line in iter(process.stdout.readline, ''):
                        sys.stdout.write(line)
                        f.write(line)
                    shutil.rmtree(folder_direct)
                    root_disk.destroy()
                    eg.msgbox("Disk Wriggler Async IO test is completed and results are captured") 
                    root.deiconify() 
                    
            elif (iotype == 'Cached_IO'):
                folder_direct=r+':\\Disk_Wriggler\\'+date_string+'Cached_IO'
                os.makedirs(folder_direct)
                with open('C:/AUPEDACO/Disk_Wriggler/result/Result_Disk_Wriggler_Cached_IO_'+date_string +'.txt', 'wb') as f:
              
                    process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n",frames,"-o",folder_direct],stdout=subprocess.PIPE)
                    for line in iter(process.stdout.readline, ''):
                        sys.stdout.write(line)
                        f.write(line)
                    shutil.rmtree(folder_direct)
                    root_disk.destroy()   
                    
                    eg.msgbox("Disk Wriggler Async IO test is completed and results are captured") 
                    root.deiconify() 
            else:
                eg.msgbox("Select any of the check box")
                
        else:
            eg.msgbox("Enter the Number of the frames")

  
    b=Button(root_disk, text='Start_test', command=test)
    b.pack()
    b.place(x=600, y=20)

    def default_test_direct():
        
        date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
        inkscape_dir=r"C:\AUPEDACO\Disk_Wriggler\diskWriggler-1.0.1.win32"
        assert os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        folder_direct='D:\\Disk_Wriggler\\'+date_string+'D'
        print folder_direct
        os.makedirs(folder_direct)
             
                
        with open('C:/AUPEDACO/Disk_Wriggler/result/Result_Disk_Wriggler_Direct_IO_'+date_string +'.txt', 'wb') as f:
      
            process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n","50","-o",folder_direct,'-D'],stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, ''):
                sys.stdout.write(line)
                f.write(line)
            shutil.rmtree(folder_direct) 
            
            root_disk.destroy() 
            eg.msgbox("Disk Wriggler Direct Default test is completed and results are captured") 
            root.deiconify()         
            
    d=Button(root_disk, text='Start_Direct_Default_test', command=default_test_direct)
    d.pack()
    d.place(x=200, y=420)
    
    def default_test_Cached():
        date_string = datetime.datetime.now().strftime("%Y-%m-%d_%H %M")
        
         
        inkscape_dir=r"C:\AUPEDACO\Disk_Wriggler\diskWriggler-1.0.1.win32"
        assert os.path.isdir(inkscape_dir)
        os.chdir(inkscape_dir)
        folder_direct='D:\\Disk_Wriggler\\'+date_string+'C'
        print folder_direct
        os.makedirs(folder_direct)
             
                
        with open('C:/AUPEDACO/Disk_Wriggler/result/Result_Disk_Wriggler_Cached_IO_'+date_string +'.txt', 'wb') as f:
      
            process= subprocess.Popen(['diskWriggler.exe',"-HD","-t","-n","50","-o",folder_direct],stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, ''):
                sys.stdout.write(line)
                f.write(line)
            shutil.rmtree(folder_direct)    
            root_disk.destroy()          
            eg.msgbox("Disk Wriggler Cached Default is completed and results are captured") 
            root.deiconify()         
            
    d=Button(root_disk, text='Start_Cached_Default_test', command=default_test_Cached)
    d.pack()
    d.place(x=200, y=480)
    def back():
        root_disk.destroy()
        root.deiconify()
  
    b1=Button(root_disk, text='back', command=back)
    b1.pack()
    b1.place(x=60, y=680)
    #sys.exit(0)
   
bu= Button(root, text='Start', command=tools)
bu.pack(anchor = "e", padx=40,pady = 40)

def help_text():
    root_help= Tk()
    myTextWidget= Text(root_help) # set up a text widget as a root (window) child

    myFile=file("Help.txt") # get a file handle
    myText= myFile.read() # read the file to variable
    myFile.close() # close file handle

    myTextWidget.insert(0.0,myText) # insert the file's text into the text widget

    myTextWidget.pack(expand=1, fill=BOTH)


bun= Button(root, text='Help', command=help_text)
bun.pack(anchor = "e", padx=40,pady = 40)
def RAID():
    root.withdraw()
    root_disk =Tkinter.Tk()
    root_disk.title("RAID TOOL")
    f = Frame(root_disk, width=1000, bg="blue")
    root_disk.geometry("700x700")
    f.pack_propagate(0)

    def create_raid():
        try:
            root_disk.withdraw()
            root_sel =Tkinter.Tk()
            root_sel.title("RAID TOOL")
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
        root_cr.title("RAID TOOL")
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
            root_dis.title("RAID TOOL")
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
            root_sel.title("RAID TOOL")
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
                root_sel.title("RAID TOOL")
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
        root_di.title("RAID TOOL")
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
    d.place(x=100, y=500)
    def partition():
        root_disk.withdraw()
        eg.msgbox("There are no RAID Levels to create partition.") 
        root_disk.deiconfy() 	 

    d = Button(root_disk, text='Create Partition', command=partition)
    d.pack()
    d.place(x=100, y=400)
    def back_raid():
        root_disk.withdraw()
        root.deiconify()
    
    d = Button(root_disk, text='BACK', command=back_raid)
    d.pack()
    d.place(x=50, y=600)

d =Button(root, text='RAID', command=RAID)
d.pack()
d.place(x=625, y=400)

root.mainloop()


