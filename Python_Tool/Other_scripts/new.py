from Tkinter import *
import tktable

class App:

    def __init__(self, master): 
        """master is the top level window"""


        master.geometry(("%dx%d")%(250,60))
        master.title("Test")

        frame = Frame(master)
        frame.pack()

        var = tktable.ArrayVar(frame)
        for y in range(6):
            for x in range(6):
                index = "%i,%i" % (y, x)
                var[index] = index

        label = Label(frame, text="test2")
        label.pack(side = 'top', fill = 'x')

        quit = Button(frame, text="QUIT", command=root.destroy)
        quit.pack(side = 'bottom', fill = 'x')

        test = tktable.Table(frame,
                 rows=6,
                 cols=6,
                 state='disabled',
                 width=6,
                 height=6,
                 titlerows=1,
                 titlecols=0,
                 roworigin=0,
                 colorigin=0,
                 selectmode='browse',
                 selecttype='row',
                 rowstretch='unset',
                 colstretch='last',
                 flashmode='on',
                 variable=var,
                 usecommand=0)
        test.pack(expand=1, fill='both')
        test.tag_configure('sel', background = 'yellow')
        test.tag_configure('active', background = 'blue')
        test.tag_configure('title', anchor='w', bg='red', relief='sunken')


root = Tk()
app = App(root)
root.mainloop()