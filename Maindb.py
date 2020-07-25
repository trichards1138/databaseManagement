#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database keeper: Is an app to organize your DVD's and CD's (or any other hobby
set) and keep track of them in case you are looking to buy a new DVD and don't 
remember if you already have it (or a tool or cloth swatch :) etc) either stand-alone 
or contained within a movie or music collection.

Main file: This contains the main window and sets everything in motion.

Copyright 2020 by Perfection Quest Software
"""

from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkinter import messagebox
import dbFileSupport as fsup
import sqliteSupport as sqll
import MaindbSupport as ms
import getINIinfo as gini
import AddRow as ar
import helpdisplay as hp

# Delete any previous entries in the file table menu
def deleteprevmenu():
    index = filedatabasemenu.index(END) # end index
    while index > 1:    # Step backward from the end
        filedatabasemenu.delete(index)    #the label is valid so it exists
        index -= 1                        # delete it and go to the next
    return

# Add the table list from a newly opened file to the "File_Table" menu
def addtablemenu(sql,fs, ReadingFile):
    secnum = 2     #if we are reading a file, we've deleted the previous menu of tables
    if ReadingFile: # so we can just start after the separator (index 1)
        for tname in sql.tablelist:
            filedatabasemenu.add_radiobutton(label=tname, 
                command=lambda:ms.selectnewfiledb(dvd_List,stat1,stat2,sql,fs,combolist,selection), variable=selection, value=secnum, font=myFont2)
            secnum += 1
        filedatabasemenu.invoke(2)  # Go ahead and load the table that is first in the list and set focus
    else: #Just adding an entry from the menu
        secnum = filedatabasemenu.index(END) + 1    #Insert the new entry on the end of the existing menu
        filedatabasemenu.add_radiobutton(label=sql.table, 
                command=lambda:ms.selectnewfiledb(dvd_List,stat1,stat2,sql,fs,combolist,selection), variable=selection, value=secnum, font=myFont2)
    return

# Update the "INI_Tables" menu with any added INI sections
def updateinimenu(sql,fs,iniList):
    secnum = fs.numsec - 1      # set the section number to the end of the menu list
    inidatabasemenu.add_radiobutton(label=iniList[0],   # add a new entry with that section number
                command=lambda:ms.selectnewinidb(dvd_List,stat1,stat2,sql,fs,combolist,selection), variable=selection, value=secnum, font=myFont2)
    return

# Set up the main window
root=Tk()
root.wm_title("Database Management")
root.geometry("674x600")

myFont1 = Font(family="Times", size=16, weight="bold")
myFont2 = Font(family="verdana", size=11, weight="bold")

#Predefine some variables
dvd_List = None         #Main List Box
stat1 = StringVar()     #status bar strings
stat2 = StringVar()
fs = None               #file support class variable
sql = None              #database support class variable
combolist = []

#Define the Menu Bar contents and their action functions
menubar = Menu(root)
menubar.config(font=myFont2)
filemenu = Menu(menubar, tearoff=0)     # File menu, spaces added to make it look nicer
filemenu.add_command(label="  New... ", command=lambda:ms.Newdbfile(dvd_List,stat1,stat2,sql,fs,deleteprevmenu), font=myFont2)
filemenu.add_command(label="  Open...", command=lambda:ms.Opendbfile(dvd_List,stat1,stat2,sql,fs,addtablemenu,deleteprevmenu), font=myFont2) 
filemenu.add_command(label="  Close", command=lambda:ms.fclose(dvd_List,stat1,stat2,sql), font=myFont2) 
filemenu.add_command(label="  SaveAs...", command=lambda:ms.SaveAsdbfile(sql,fs), font=myFont2)
filemenu.add_separator()
filemenu.add_command(label="  Exit  ", command=root.destroy, font=myFont2)
menubar.add_cascade(label=" File", menu=filemenu, font=myFont2)

# This menu shows the section in the INI file (and any added sections)
inidatabasemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label=" INI_Tables ", menu=inidatabasemenu, font=myFont2)
inidatabasemenu.add_checkbutton(label="Add Section to INI...", command=lambda:gini.inisectioninfo(fs, sql, updateinimenu, True), font=myFont2 )
inidatabasemenu.add_separator()

# This menu shows the database tables in the current db file
filedatabasemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File_Tables", menu=filedatabasemenu, font=myFont2)
filedatabasemenu.add_checkbutton(label="Create New Table...", command=lambda:gini.inisectioninfo(fs, sql, addtablemenu, False), font=myFont2 )
filedatabasemenu.add_separator()

# A single command in the menu that repaints the Listbox
menubar.add_command(label="Show All", command=lambda:ms.dbview(dvd_List,stat2,sql), font=myFont2)

# Help menu 
helpmenu = Menu(menubar, tearoff=0)                 # Use messageboxes to implement
helpmenu.add_command(label="Help Index...", command=hp.hdisplay, font=myFont2)
helpmenu.add_command(label="About...", command=ms.AboutBox, font=myFont2)
menubar.add_cascade(label="Help", menu=helpmenu, font=myFont2)

# Search the database for entries that match one of four entered parameters.
# The table schema (combo boxes) and descriptor parameters (entries)
b1=Button(root, text='Search Database', 
          command= lambda: ms.search(dvd_List, stat2, descr1.get(), descr2.get(), descr3.get(), descr4.get(),
            header1.get(), header2.get(), header3.get(), header4.get(), sql))
b1.place(x = 530, y = 10, width=120, height=30)
b1.configure(bd=2, relief=RAISED)

# Message for user
SearchLabel=Label(root,text="Enter Parameter Set, Then Press Search:")
SearchLabel.configure(font=myFont1)
SearchLabel.place(x = 20, y = 20, height=30)

# A sunken frame that makes the search parameters stand out
entryFrame = Frame(root, borderwidth = 5)
entryFrame.place(x=10, y=50, height=100, width=640)
entryFrame.config(bd=3, relief=SUNKEN)

# The next four combobox-entry sections get the serarch parameters from the
# user
header1 = StringVar()
schema1=ttk.Combobox(entryFrame, textvariable = header1, state="readonly")
schema1.place(x = 20, y = 10, width=140, height=30)
schema1.configure(font=myFont2)

descr1=StringVar()
dvde1=Entry(entryFrame,textvariable=descr1)
dvde1.place(x = 160, y = 10, width=140, height=30)
dvde1.configure(font=myFont2)

header2 = StringVar()
schema2=ttk.Combobox(entryFrame, textvariable = header2, state="readonly")
schema2.place(x = 330, y = 10, width=140, height=30)
schema2.configure(font=myFont2)

descr2=StringVar()
dvde2=Entry(entryFrame,textvariable=descr2)
dvde2.place(x = 470, y = 10, width=140, height=30)
dvde2.configure(font=myFont2)

header3 = StringVar()
schema3=ttk.Combobox(entryFrame, textvariable = header3, state="readonly")
schema3.place(x = 20, y = 50, width=140, height=30)
schema3.configure(font=myFont2)

descr3=StringVar()
dvde3=Entry(entryFrame,textvariable=descr3)
dvde3.place(x = 160, y = 50, width=140, height=30)
dvde3.configure(font=myFont2)

header4 = StringVar()
schema4=ttk.Combobox(entryFrame, textvariable = header4, state="readonly")
schema4.place(x = 330, y = 50, width=140, height=30)
schema4.configure(font=myFont2)

descr4=StringVar()
dvde4=Entry(entryFrame,textvariable=descr4)
dvde4.place(x = 470, y = 50, width=140, height=30)
dvde4.configure(font=myFont2)

# Another message to user
ListLabel=Label(root,text="Single Click Selects, Double Click Edits:")
ListLabel.place(x = 20, y = 170, height=30)
ListLabel.configure(font=myFont1)

# A more convienient way to pass the combos as parameters
combolist = [schema1,header1,descr1,schema2,header2,descr2,schema3,header3,descr3,schema4,header4,descr4]

# Another frame surrounding the Listbox
listboxframe = Frame(root)
listboxframe.place(x=10, y=200, height=320, width=650)

# Definitions of the Listbox
vscrollbar = Scrollbar(listboxframe, orient=VERTICAL)   # vertical scrollbar
hscrollbar = Scrollbar(listboxframe, orient=HORIZONTAL) # horizontal scrollbar
# Instantiate the Listbox itself with scroll bars set
dvd_List = Listbox(listboxframe, yscrollcommand=vscrollbar.set,
            xscrollcommand=hscrollbar.set, selectmode = SINGLE)
dvd_List.place(x = 0, y = 0, width=625, height=300)
dvd_List.config(bd=3, relief=SUNKEN)
dvd_List.configure(font=myFont2)
# A single-click on an entry just selects it
dvd_List.bind("<<ListboxSelect>>", ms.donothing())
# A double-click goes to the add_row to edit the entry
dvd_List.bind('<Double-1>', lambda x:ar.add_row(myFont2, dvd_List, stat2, sql, True))
vscrollbar.config(command=dvd_List.yview)
vscrollbar.place(x=625, y=0, height=300, width=15)
hscrollbar.config(command=dvd_List.xview)
hscrollbar.place(x=0, y=300, height=15, width=625)

# Select to add a new entry to the Listbox (not yet defined) and the database
b2=Button(root, text='Add Entry', command=lambda:ar.add_row(myFont2, dvd_List,stat2,sql, False))
b2.place(x = 560, y = 160, width=90, height=30)
b2.configure(bd=2, relief=RAISED)

# Delete an entry from the listbox and the database
b3=Button(root, text='Delete Entry', command = lambda: ms.delete(dvd_List,stat2,sql))
b3.place(x = 450, y = 160, width=100, height=30)
b3.configure(bd=2, relief=RAISED)

# Lable for the Status Bar
statusbarLabel=Label(root,text="Status Bar:")
statusbarLabel.place(x = 20, y = 515, height=30)
statusbarLabel.configure(font=myFont1)

# Another frame surrounding the status bar
statusframe = Frame(root)
statusframe.place(x=10, y=545, height=35, width=645)
statusframe.config(bd=3, relief=SUNKEN)

# Labels in the status bar.  This shows the current db file
statusLabel1=Label(statusframe,textvariable=stat1)
statusLabel1.place(x = 0, y = 0, height=29, width=400)
statusLabel1.configure(font=myFont2, bd=2, relief=RIDGE, anchor=W)

# This shows the number of entries in the Listbox
statusLabel2=Label(statusframe,textvariable=stat2)
statusLabel2.place(x = 400, y = 0, height=29, width=240)
statusLabel2.configure(font=myFont2, bd=2, relief=RIDGE, anchor = W)

Path = ""       #predefine for structure below
dbname = ""
dbfname = ""

fs = fsup.dbfileSupport()   #open the file support class
sql = sqll.dbsupport()      #open the database support class
selection = IntVar()
selection.set(0)

fs.get_items()      # Get sections in the INI file
if fs.numsec > 0:   # If there are sections present
    secnum = 0      
    #add all of the database sections in the INI file to the menu
    while secnum < fs.numsec:
        inidatabasemenu.add_radiobutton(label=fs.items[secnum][0], 
                command=lambda:ms.selectnewinidb(dvd_List,stat1,stat2,sql,fs,combolist,selection), variable=selection, value=secnum, font=myFont2)
        secnum += 1
    inidatabasemenu.invoke(2)   #Set focus to the first entry
    #set up the titles for the search parameters
    secnum=0
    #send the combo boxes to the selectnew and update there
    ms.selectnewinidb(dvd_List,stat1,stat2,sql,fs,combolist,selection)
else:
    messagebox.showinfo(title="Empty INI File", 
                message = "There are no sections defined in the INI file\n or it is missing.  Open a db file to continue!")  

root.config(bd=4, relief=RAISED, menu=menubar )
root.mainloop()