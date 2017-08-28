#!/usr/bin/env python
__author__ = "levi mangarin"
__copyright__ = "cc 2016 levim"
__credits__ = ["levi mangarin", "scales"]
__maintainer__ = "levi mangarin"
__email__ = "markmangarin@gmail.com"
__status__ = "dev"


import csv
import time
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

class App():
    def __init__(self, master=None):
        self.master = ttk.Frame(master, padding="4 3 12 12")
        master.title("jb2")
        self.master.grid(column=0, row=0, sticky=(N, W, E, S))  #all dirs to center
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        # Simple status flag
        # False mean the self.timer is not running
        # True means the self.timer is running (counting)
        self.state = False 
        
        # Our time structure [min, sec, centsec]
        self.timer = [0, 0, 0]
        # The format is padding all the 
        self.pattern = '{0:02d}:{1:02d}:{2:02d}'
        
        self.judge = StringVar()
        self.ytLink = StringVar()
        self.scorePos = IntVar(0) 
        self.scoreNeg = IntVar(0)
        self.scoreTitle = ["Time", "Click"]
        self.score = [['00:00:00', 0]]
        
        self.judgeEntry = ttk.Entry(self.master, width=7, textvariable=self.ytLink)
        self.ytLink.set("yt link")
        self.judgeEntry.grid(column=3, row=1, sticky=(W, E))
        self.ytEntry = ttk.Entry(self.master, width=7, textvariable=self.judge)
        self.judge.set("Judge")
        self.ytEntry.grid(column=2, row=1, sticky=(W, E))
        
        self.timeText = ttk.Label(self.master, text="00:00:00")
        self.timeText.grid(column=1, row=1, sticky=(W, N))
        self.startButton = ttk.Button(self.master, text='Start', command=self.start)
        self.startButton.grid(column=1, row=4)
        self.pauseButton = ttk.Button(self.master, text='Pause', command=self.pause)
        self.pauseButton.grid(column=3, row=4)
        self.resetButton = ttk.Button(self.master, text='Reset', command=self.reset)
        self.resetButton.grid(column=4, row=4)
        
        ttk.Label(self.master, textvariable=self.scoreNeg).grid(column=1, row=3, sticky=(W, E))
        ttk.Label(self.master, textvariable=self.scorePos).grid(column=2, row=3, sticky=(W, E))
        ttk.Button(self.master, text="+", command=self.clickerPos).grid(column=2, row=2, sticky=W)
        ttk.Button(self.master, text="-", command=self.clickerNeg).grid(column=1, row=2, sticky=W)
        
        ttk.Button(self.master, text='Save Score', command=self.file_save).grid(column=4, row=2, sticky=W)
       
        ttk.Label(self.master, text="score").grid(column=3, row=2, sticky=W)
        
        for child in self.master.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        self.judgeEntry.focus()
        self.ytEntry.focus()

        master.bind("f", self.clickerPos) #bind return to clicker proc
        master.bind("d", self.clickerNeg) #bind return to clicker proc
        master.bind("k", self.clickerPos) #bind return to clicker proc
        master.bind("j", self.clickerNeg) #bind return to clicker proc
        master.bind("p", self.pause) #bind return to clicker proc
        master.bind("q", self.reset) #bind return to clicker proc
        master.bind("y", self.start) #bind return to clicker proc
        master.bind('<Return>', self.start) #bind return to clicker proc
        self.update_timeText()
        
    #clicker methods
    def metadata(self):
        try:
            value = float(self.metadata.get())
        except ValueError:
            pass
    
    def clickerPos(self, event=None):
        try:
            self.scorePos.set(self.scorePos.get() + 1)
            Tk.update_idletasks(root)
    
            self.score.append([self.timeString, 1])
        except ValueError:
            pass
    
    def clickerNeg(self, event=None):
        try:
            self.scoreNeg.set(self.scoreNeg.get() + 1)
            Tk.update_idletasks(root)
    
            self.score.append([self.timeString, -1])
        except ValueError:
            pass
    
    #self.timer methods
    def update_timeText(self):
        if (self.state):
            # Every time this function is called, 
            # we will increment 1 centisecond (1/100 of a second)
            self.timer[2] += 1
            
            # Every 100 centisecond is equal to 1 second
            #if (self.timer[2] >= 100):
            if (self.timer[2] >= 60): #changing to 60 due to timer calibration
                self.timer[2] = 0
                self.timer[1] += 1
            # Every 60 seconds is equal to 1 min
            if (self.timer[1] >= 60):
                self.timer[0] += 1
                self.timer[1] = 0
            # We create our time string here
            self.timeString = self.pattern.format(self.timer[0], self.timer[1], self.timer[2])
            # Update the timeText Label box with the current time
            self.timeText.configure(text=self.timeString)
            # Call the update_timeText() function after 1 centisecond
        root.after(10, self.update_timeText)
        Tk.update_idletasks(root)
    
    # To reset the self.timer to 00:00:00
    def reset(self, event=None):
        self.timer = [0, 0, 0]
        self.timeText.configure(text='00:00:00')
    
        self.scorePos.set(0)
        self.scoreNeg.set(0)
        self.score = [['00:00:00', 0]]
        self.pause()
        Tk.update_idletasks(root)
    
    # To start the self.timer
    def start(self, event=None):
        self.state = True
        Tk.update_idletasks(root)

    # To pause the self.timer
    def pause(self, event=None):
        self.state = False
        Tk.update_idletasks(root)

    def file_save(self, event=None):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return

        f.write(str(self.judge) + '\n'  + str(self.ytLink) + '\n' )
        f.write( 'Time\tClick\n' )
        for row in self.score:
            f.write( str(row[0]) )
            f.write( '\t' )
            f.write( str(row[1]) )
            f.write( '\n' )
        f.close() 

root = Tk()
app=App(root)
root.mainloop()





























































