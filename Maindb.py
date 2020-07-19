#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DVD keeper: Is an app to organize your DVD's and CD's and keep track of them
in case you are looking to buy a new DVD and don't remember if you already
have it either stand-alone or contained within a movie or music collection.
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


def deleteprevmenu():
    index = filedatabasemenu.index(END)
    while index > 1:  
        filedatabasemenu.delete(index)    #the label is valid so it exists
        index -= 1                        # delete it and go to the next
    return

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

def updateinimenu(sql,fs,iniList):
    secnum = fs.numsec - 1
    inidatabasemenu.add_radiobutton(label=iniList[0], 
                command=lambda:ms.selectnewinidb(dvd_List,stat1,stat2,sql,fs,combolist,selection), variable=selection, value=secnum, font=myFont2)
    return

root=Tk()
root.wm_title("Database Search")
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
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="  New   ", command=lambda:ms.Newdbfile(dvd_List,stat1,stat2,sql,fs,deleteprevmenu), font=myFont2)
filemenu.add_command(label="  Open  ", command=lambda:ms.Opendbfile(dvd_List,stat1,stat2,sql,fs,addtablemenu,deleteprevmenu), font=myFont2) 
filemenu.add_command(label="  SaveAs", command=lambda:ms.SaveAsdbfile(sql,fs), font=myFont2)
filemenu.add_separator()
filemenu.add_command(label="  Exit  ", command=root.destroy, font=myFont2)
menubar.add_cascade(label=" File", menu=filemenu, font=myFont2)

inidatabasemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label=" INI_Tables ", menu=inidatabasemenu, font=myFont2)
inidatabasemenu.add_checkbutton(label="Add Section to INI", command=lambda:gini.inisectioninfo(fs, sql, updateinimenu, True), font=myFont2 )
inidatabasemenu.add_separator()

filedatabasemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File_Tables", menu=filedatabasemenu, font=myFont2)
filedatabasemenu.add_checkbutton(label="Create New Table", command=lambda:gini.inisectioninfo(fs, sql, addtablemenu, False), font=myFont2 )
filedatabasemenu.add_separator()

menubar.add_command(label="Show All", command=lambda:ms.dbview(dvd_List,stat2,sql), font=myFont2)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=ms.donothing, font=myFont2)
helpmenu.add_command(label="About...", command=ms.donothing, font=myFont2)
menubar.add_cascade(label="Help", menu=helpmenu, font=myFont2)

b1=Button(root, text='Search Database', 
          command= lambda: ms.search(dvd_List, stat2, descr1.get(), descr2.get(), descr3.get(), descr4.get(),
            header1.get(), header2.get(), header3.get(), header4.get(), sql))
b1.place(x = 530, y = 10, width=120, height=30)
b1.configure(bd=2, relief=RAISED)

SearchLabel=Label(root,text="Enter Parameter Set, Then Press Search:")
SearchLabel.configure(font=myFont1)
SearchLabel.place(x = 20, y = 20, height=30)

entryFrame = Frame(root, borderwidth = 5)
entryFrame.place(x=10, y=50, height=100, width=640)
entryFrame.config(bd=3, relief=SUNKEN)

header1 = StringVar()
schema1=ttk.Combobox(entryFrame, textvariable = header1)
schema1.place(x = 20, y = 10, width=140, height=30)
schema1.configure(font=myFont2)

descr1=StringVar()
dvde1=Entry(entryFrame,textvariable=descr1)
dvde1.place(x = 160, y = 10, width=140, height=30)
dvde1.configure(font=myFont2)

header2 = StringVar()
schema2=ttk.Combobox(entryFrame, textvariable = header2)
schema2.place(x = 330, y = 10, width=140, height=30)
schema2.configure(font=myFont2)

descr2=StringVar()
dvde2=Entry(entryFrame,textvariable=descr2)
dvde2.place(x = 470, y = 10, width=140, height=30)
dvde2.configure(font=myFont2)

header3 = StringVar()
schema3=ttk.Combobox(entryFrame, textvariable = header3)
schema3.place(x = 20, y = 50, width=140, height=30)
schema3.configure(font=myFont2)

descr3=StringVar()
dvde3=Entry(entryFrame,textvariable=descr3)
dvde3.place(x = 160, y = 50, width=140, height=30)
dvde3.configure(font=myFont2)

header4 = StringVar()
schema4=ttk.Combobox(entryFrame, textvariable = header4)
schema4.place(x = 330, y = 50, width=140, height=30)
schema4.configure(font=myFont2)

descr4=StringVar()
dvde4=Entry(entryFrame,textvariable=descr4)
dvde4.place(x = 470, y = 50, width=140, height=30)
dvde4.configure(font=myFont2)

ListLabel=Label(root,text="Single Click Selects, Double Click Edits:")
ListLabel.place(x = 20, y = 170, height=30)
ListLabel.configure(font=myFont1)

combolist = [schema1,schema2,schema3,schema4]

listboxframe = Frame(root)
listboxframe.place(x=10, y=200, height=320, width=650)

vscrollbar = Scrollbar(listboxframe, orient=VERTICAL)
hscrollbar = Scrollbar(listboxframe, orient=HORIZONTAL)
dvd_List = Listbox(listboxframe, yscrollcommand=vscrollbar.set,
            xscrollcommand=hscrollbar.set, selectmode = SINGLE)
dvd_List.place(x = 0, y = 0, width=625, height=300)
dvd_List.config(bd=3, relief=SUNKEN)
dvd_List.configure(font=myFont2)
dvd_List.bind("<<ListboxSelect>>", ms.donothing())
dvd_List.bind('<Double-1>', lambda x:ar.add_row(myFont2, dvd_List, stat2, sql, True))
vscrollbar.config(command=dvd_List.yview)
vscrollbar.place(x=625, y=0, height=300, width=15)
hscrollbar.config(command=dvd_List.xview)
hscrollbar.place(x=0, y=300, height=15, width=625)

b2=Button(root, text='Add Entry', command=lambda:ar.add_row(myFont2, dvd_List,stat2,sql, False))
b2.place(x = 560, y = 160, width=90, height=30)
b2.configure(bd=2, relief=RAISED)

b3=Button(root, text='Delete Entry', command = lambda: ms.delete(dvd_List,stat2,sql))
b3.place(x = 450, y = 160, width=100, height=30)
b3.configure(bd=2, relief=RAISED)

statusbarLabel=Label(root,text="Status Bar:")
statusbarLabel.place(x = 20, y = 515, height=30)
statusbarLabel.configure(font=myFont1)

statusframe = Frame(root)
statusframe.place(x=10, y=545, height=35, width=645)
statusframe.config(bd=3, relief=SUNKEN)

#stat1 = StringVar()
statusLabel1=Label(statusframe,textvariable=stat1)
statusLabel1.place(x = 0, y = 0, height=29, width=400)
statusLabel1.configure(font=myFont2, bd=2, relief=RIDGE, anchor=W)

#stat2 = StringVar()
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

fs.get_items()
if fs.numsec > 0:
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
    
    schemaList = []
    scount = 4
    while scount < 12:
        schemaList.append(fs.items[0][scount])
        scount += 1
    ms.fillinCombo(schema1, schemaList)
    ms.fillinCombo(schema2, schemaList)
    ms.fillinCombo(schema3, schemaList)
    ms.fillinCombo(schema4, schemaList)
else:
    messagebox.showinfo(title="Empty INI File", 
                message = "There are no sections defined in the INI file\n or it is missing.  Open a db file to continue!")  

root.config(bd=4, relief=RAISED, menu=menubar )
root.mainloop()