#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database keeper: Is an app to organize your DVD's and CD's (or any other hobby
set) and keep track of them in case you are looking to buy a new DVD and don't 
remember if you already have it (or a tool or cloth swatch :) etc) either stand-alone 
or contained within a movie or music collection.

getINIinfo - A popup window to get information for a new INI section or a new database
table (table name and schema - as well as path and filename)

Copyright 2020 by Perfection Quest Software
"""
from tkinter import *
from tkinter.font import Font
import ntpath

# Define a new set of information that can update the INI file or be added
# to a selected file.  Selecting either "Add Section to INI" or "Create New Table"
# will open this window.  The user enters the Name (INI only), table name, path and 
# filename (INI only), and the schema that matches the table.
# 
# Note: the table name and schema must match the table and schema in the file or
#       database operations will be impossible
def inisectioninfo(fs, sql, menuadd, AddingINI):
    #set some initial values in a list
    iniList = []
    iniList.append("Place Keeper")
    iniList.append(sql.table)
    iniList.append(ntpath.dirname(sql.sqldbfname))
    iniList.append(ntpath.basename(sql.sqldbfname))
    iniList.append(sql.schema)
    # even though number of sections (numsec) is not used for the INI file
    # it is used for other bookkeeping
    iniList.append(fs.numsec)

    #initialize the popup window
    isi = Toplevel()
    if AddingINI:
        isi.wm_title("Get INI Section Info")    # if called from "INI_Tables"
    else:
        isi.wm_title("Create New DB Table")     # if called from "File_Tables"
    isi.geometry("560x450") 
    isi.config(bd=5, relief=RAISED)

    iniFont = Font(family="verdana", size=11, weight="bold")

    # Entry used in the INI only.  This entry is diplayed in the INI_Tables menu
    iniName = Label(isi,text="INI Name for Database:")
    iniName.configure(font=iniFont)
    iniName.place(x = 20, y = 20, height=30)

    iniNameS=StringVar()
    iniNameS.set(iniList[0])
    iniNameE=Entry(isi,textvariable=iniNameS)
    iniNameE.place(x = 280, y = 20, width=250, height=30)
    iniNameE.configure(font=iniFont)
    if not AddingINI:   # Entry not used in File_Tables menu
        iniNameE.configure(state='disabled')

    # The database Table name that names the database in the file
    # Used in both INI and File Tables
    iniTable = Label(isi,text="DataBase Table:")
    iniTable.configure(font=iniFont)
    iniTable.place(x = 20, y = 50, height=30)

    iniTableS=StringVar()
    iniTableS.set(iniList[1])
    iniTableE=Entry(isi,textvariable=iniTableS)
    iniTableE.place(x = 280, y = 50, width=250, height=30)
    iniTableE.configure(font=iniFont)

    # The Path and File name is an entry in the INI.  It is used to 
    # open the appropriate file for the database Table selected
    iniPath = Label(isi,text="DataBase File Path:")
    iniPath.configure(font=iniFont)
    iniPath.place(x = 20, y = 80, height=30)
    
    iniPathS=StringVar()
    iniPathS.set(iniList[2])
    iniPathE=Entry(isi,textvariable=iniPathS)
    iniPathE.place(x = 280, y = 80, width=250, height=30)
    iniPathE.configure(font=iniFont)
    if not AddingINI:   # If the user opened a file, all of the tables are 
        iniPathE.configure(state='disabled')    # in the same file

    iniFname = Label(isi,text="DataBase File Name:")
    iniFname.configure(font=iniFont)
    iniFname.place(x = 20, y = 110, height=30)

    iniFnameS=StringVar()
    iniFnameS.set(iniList[3])
    iniFnameE=Entry(isi,textvariable=iniFnameS)
    iniFnameE.place(x = 280, y = 110, width=250, height=30)
    iniFnameE.configure(font=iniFont)
    if not AddingINI:
        iniFnameE.configure(state='disabled')

    # The next eight entries define the database schema
    # The schema entered must match the schema in the 
    # database Table above if it exists already
    iniSchema1 = Label(isi,text="DataBase Schema1 (Value1):")
    iniSchema1.configure(font=iniFont)
    iniSchema1.place(x = 20, y = 150, height=30)

    iniSchema1S=StringVar()
    iniSchema1S.set(iniList[4][0])
    iniSchema1E=Entry(isi,textvariable=iniSchema1S)
    iniSchema1E.place(x = 280, y = 150, width=250, height=30)
    iniSchema1E.configure(font=iniFont)

    iniSchema2 = Label(isi,text="DataBase Schema2 (Value2):")
    iniSchema2.configure(font=iniFont)
    iniSchema2.place(x = 20, y = 180, height=30)

    iniSchema2S=StringVar()
    iniSchema2S.set(iniList[4][1])
    iniSchema2E=Entry(isi,textvariable=iniSchema2S)
    iniSchema2E.place(x = 280, y = 180, width=250, height=30)
    iniSchema2E.configure(font=iniFont)

    iniSchema3 = Label(isi,text="DataBase Schema3 (Value3):")
    iniSchema3.configure(font=iniFont)
    iniSchema3.place(x = 20, y = 210, height=30)

    iniSchema3S=StringVar()
    iniSchema3S.set(iniList[4][2])
    iniSchema3E=Entry(isi,textvariable=iniSchema3S)
    iniSchema3E.place(x = 280, y = 210, width=250, height=30)
    iniSchema3E.configure(font=iniFont)

    iniSchema4 = Label(isi,text="DataBase Schema4 (Value4):")
    iniSchema4.configure(font=iniFont)
    iniSchema4.place(x = 20, y = 240, height=30)

    iniSchema4S=StringVar()
    iniSchema4S.set(iniList[4][3])
    iniSchema4E=Entry(isi,textvariable=iniSchema4S)
    iniSchema4E.place(x = 280, y = 240, width=250, height=30)
    iniSchema4E.configure(font=iniFont)

    iniSchema5 = Label(isi,text="DataBase Schema5 (Value5):")
    iniSchema5.configure(font=iniFont)
    iniSchema5.place(x = 20, y = 270, height=30)

    iniSchema5S=StringVar()
    iniSchema5S.set(iniList[4][4])
    iniSchema5E=Entry(isi,textvariable=iniSchema5S)
    iniSchema5E.place(x = 280, y = 270, width=250, height=30)
    iniSchema5E.configure(font=iniFont)

    iniSchema6 = Label(isi,text="DataBase Schema6 (Value6):")
    iniSchema6.configure(font=iniFont)
    iniSchema6.place(x = 20, y = 300, height=30)

    iniSchema6S=StringVar()
    iniSchema6S.set(iniList[4][5])
    iniSchema6E=Entry(isi,textvariable=iniSchema6S)
    iniSchema6E.place(x = 280, y = 300, width=250, height=30)
    iniSchema6E.configure(font=iniFont)

    iniSchema7 = Label(isi,text="DataBase Schema7 (Value7):")
    iniSchema7.configure(font=iniFont)
    iniSchema7.place(x = 20, y = 330, height=30)

    iniSchema7S=StringVar()
    iniSchema7S.set(iniList[4][6])
    iniSchema7E=Entry(isi,textvariable=iniSchema7S)
    iniSchema7E.place(x = 280, y = 330, width=250, height=30)
    iniSchema7E.configure(font=iniFont)

    iniSchema8 = Label(isi,text="DataBase Schem8 (Value8):")
    iniSchema8.configure(font=iniFont)
    iniSchema8.place(x = 20, y = 360, height=30)

    iniSchema8S=StringVar()
    iniSchema8S.set(iniList[4][7])
    iniSchema8E=Entry(isi,textvariable=iniSchema8S)
    iniSchema8E.place(x = 280, y = 360, width=250, height=30)
    iniSchema8E.configure(font=iniFont)

    # routine to prepare all of the data entered by the user
    # and then insert it into the appropriate places
    def iniPrepare():   
        templist = []
        iniList[0] = iniNameS.get()
        iniList[1] = iniTableS.get()
        iniList[2] = iniPathS.get()
        iniList[3] = iniFnameS.get()
        templist.append(iniSchema1S.get()) 
        templist.append(iniSchema2S.get()) 
        templist.append(iniSchema3S.get()) 
        templist.append(iniSchema4S.get()) 
        templist.append(iniSchema5S.get()) 
        templist.append(iniSchema6S.get()) 
        templist.append(iniSchema7S.get()) 
        templist.append(iniSchema8S.get()) 
        iniList[4] = tuple(templist)
        if AddingINI:   # If adding to the db.ini file
            if fs.addsec2ini(iniList):  
                #if successful adding the section, add it to the menu
                menuadd(sql,fs,iniList)
            isi.destroy()   # destroy the window and return
        else:   # If adding a table to the file "Table list"
            sql.table = iniList[1]  # We need the Table name
            sql.schema = iniList[4] # and matching schema
            sql.dbcreatetable()     # create the table in the file if not there already
            sql.dbtablelist()       # This adds the new name to the table list
            sql.getschema()         # Adds the schema to the master schema list
            menuadd(sql,fs, False)  # Adds table name to the menu
            isi.destroy()           # Destroy the window and return
        return
        
        

    if AddingINI:   # Button named appropriately for INI section add
        b1=Button(isi, text='Add to INI', command=iniPrepare) 
        b1.place(x = 410, y = 400, width=120, height=30)
        b1.configure(bd=2, relief=RAISED)
    else:           # Likewise for database table addition
        b1=Button(isi, text='Create Initial Table', command=iniPrepare) 
        b1.place(x = 370, y = 400, width=160, height=30)
        b1.configure(bd=2, relief=RAISED)        
    
    isi.mainloop()
    return

