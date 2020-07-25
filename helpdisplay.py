#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database keeper: Is an app to organize your DVD's and CD's (or any other hobby
set) and keep track of them in case you are looking to buy a new DVD and don't 
remember if you already have it (or a tool or cloth swatch :) etc) either stand-alone 
or contained within a movie or music collection.

hdisplay - A popup window to provide a help system for the user.  The section selected
by the user is searched in the help file and displayed in a popup widow.

Copyright 2020 by Perfection Quest Software
"""
from tkinter import *
from tkinter.font import Font

# Display the section of help selected by the usre
def hdisplay():
    
    #initialize the popup window
    dbhelp = Toplevel()
    dbhelp.wm_title("Database Management Help")
    dbhelp.geometry("730x600") 
    dbhelp.config(bd=5, relief=RAISED)

    dbhelpFont = Font(family="Times", size=11)

    vscrollbar = Scrollbar(dbhelp, orient=VERTICAL)   # vertical scrollbar
    
    txt_edit = Text(dbhelp, relief=SUNKEN ,bd=3, yscrollcommand=vscrollbar.set)
    txt_edit.place(x=150, y=0, height=590, width=540)
    txt_edit.configure(state="normal", font=dbhelpFont, wrap=WORD, spacing2=4, spacing3=4)

    vscrollbar.config(command=txt_edit.yview)
    vscrollbar.place(x=700, y=0, height=590, width=15)

    hfile = open("help.txt", "r")

    treeFrame = Frame(dbhelp, borderwidth = 3)  
    treeFrame.place(x=0, y=0, height=590, width=150)  
    treeFrame.config(relief=RAISED)

    helptext = hfile.read()
    txt_edit.insert(END, helptext)

    def findposition(sectionNumber):
        sectiontags = ["1. ", "1.1", "1.2", "1.3", "1.4", "2. ", "2.1", "2.2", "2.3", "2.4",
                        "3. ", "3.1", "4. "]
        textptr = 0
        textend = len(helptext)
        txt_edit.delete("1.0", END)
        while True:
            if helptext[textptr:textptr+3] == sectiontags[sectionNumber]:
                break
            else:
                textptr += 1
        txt_edit.insert(END, helptext[textptr:textend])
        return

    db_overview = Button(treeFrame, text="DB Overview", command=lambda: findposition(0))
    db_overview.place( x=10, y=10, height=25, width=120)

    Row_Addition = Button(treeFrame, text="Add Item", command=lambda: findposition(1))
    Row_Addition.place( x=30, y=34, height=25, width=100)

    Row_Deletion = Button(treeFrame, text="Del Item", command=lambda: findposition(2))
    Row_Deletion.place( x=30, y=58, height=25, width=100)

    Row_Search = Button(treeFrame, text="Search Items", command=lambda: findposition(3))
    Row_Search.place( x=30, y=82, height=25, width=100)

    Row_edit = Button(treeFrame, text="Edit Items", command=lambda: findposition(4))
    Row_edit.place( x=30, y=106, height=25, width=100)


    File_Operations = Button(treeFrame, text="File Operations", command=lambda: findposition(5))
    File_Operations.place( x=10, y=140, height=25, width=120)

    FOpen = Button(treeFrame, text="File Open", command=lambda: findposition(6))
    FOpen.place( x=30, y=164, height=25, width=100)

    FNew = Button(treeFrame, text="File New", command=lambda: findposition(7))
    FNew.place( x=30, y=188, height=25, width=100)

    FClose = Button(treeFrame, text="File Close", command=lambda: findposition(8))
    FClose.place( x=30, y=212, height=25, width=100)

    FSaveAs = Button(treeFrame, text="File SaveAs", command=lambda: findposition(9))
    FSaveAs.place( x=30, y=236, height=25, width=100)


    INI_Overview = Button(treeFrame, text="INI Overview", command=lambda: findposition(10))
    INI_Overview.place( x=10, y=280, height=25, width=120)

    INI_Additions = Button(treeFrame, text="Add Section", command=lambda: findposition(11))
    INI_Additions.place( x=30, y=304, height=25, width=100)


    Mobile_Setup = Button(treeFrame, text="Mobile Dev Setup", command=lambda: findposition(12))
    Mobile_Setup.place( x=10, y=338, height=25, width=120)

    Exitb = Button(treeFrame, text="Exit", command=dbhelp.destroy)
    Exitb.place( x=10, y=546, height=25, width=120)

    dbhelp.mainloop()
    return

