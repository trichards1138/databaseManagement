#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DVD keeper: Is an app to organize your DVD's and CD's and keep track of them
in case you are looking to buy a new DVD and don't remember if you already
have it either stand-alone or contained within a movie or music collection.

File Support includes finding the directory and filename of the selected 
database and creating a new db if the user desires.
"""
from tkinter import *
import sqliteSupport as sqll
import MaindbSupport as ms

def add_row(gdbFont, dbListBox, stat2, sql, IsSelection):

     
    dbadd = Toplevel()
    dbadd.wm_title("Add New Data Base Entry")
    dbadd.geometry("700x400") 
    dbadd.config(bd=4, relief=RAISED)

    value = []  #make this a global so we can send it to update
    myschema = sql.schema
       
    schema1l=StringVar()
    schema1Label=Label(dbadd,textvariable=schema1l)
    schema1Label.place(x = 20, y = 20, height=30)
    schema1Label.configure(font=gdbFont)
    schema1l.set("Enter " + myschema[0] + ":")

    descriptor1 = StringVar()
    dvde1=Entry(dbadd,textvariable=descriptor1, width=60)
    dvde1.place(x = 300, y = 20, width=370, height=30)
    dvde1.configure(font=gdbFont)

    schema2l=StringVar()
    schema2Label=Label(dbadd,textvariable=schema2l)
    schema2Label.place(x = 20, y = 60, height=30)
    schema2Label.configure(font=gdbFont)
    schema2l.set("Enter "+myschema[1]+':')

    descriptor2=StringVar()
    dvde2=Entry(dbadd,textvariable=descriptor2, width=60)
    dvde2.place(x = 300, y = 60, width=370, height=30)
    dvde2.configure(font=gdbFont)

    schema3l=StringVar()
    schema3Label=Label(dbadd,textvariable=schema3l)
    schema3Label.place(x = 20, y = 100, height=30)
    schema3Label.configure(font=gdbFont)
    schema3l.set("Enter "+myschema[2]+':')

    descriptor3=StringVar()
    dvde3=Entry(dbadd,textvariable=descriptor3, width=60)
    dvde3.place(x =300, y = 100, width=370, height=30)
    dvde3.configure(font=gdbFont)

    schema4l=StringVar()
    schema4Label=Label(dbadd,textvariable=schema4l)
    schema4Label.place(x = 20, y = 140, height=30)
    schema4Label.configure(font=gdbFont)
    schema4l.set("Enter "+myschema[3]+':')

    descriptor4=StringVar()
    dvde4=Entry(dbadd,textvariable=descriptor4, width=60)
    dvde4.place(x = 300, y = 140, width=370, height=30)
    dvde4.configure(font=gdbFont)
    
    schema5l=StringVar()
    schema5Label=Label(dbadd,textvariable=schema5l)
    schema5Label.place(x = 20, y = 180, height=30)
    schema5Label.configure(font=gdbFont)
    schema5l.set("Enter "+myschema[4]+':')

    descriptor5=StringVar()
    dvde5=Entry(dbadd,textvariable=descriptor5, width=60)
    dvde5.place(x = 300, y = 180, width=370, height=30)
    dvde5.configure(font=gdbFont)

    schema6l=StringVar()
    schema6Label=Label(dbadd,textvariable=schema6l)
    schema6Label.place(x = 20, y = 220, height=30)
    schema6Label.configure(font=gdbFont)
    schema6l.set("Enter "+myschema[5]+':')

    descriptor6=StringVar()
    dvde6=Entry(dbadd,textvariable=descriptor6, width=60)
    dvde6.place(x = 300, y = 220, width=370, height=30)
    dvde6.configure(font=gdbFont)

    schema7l=StringVar()
    schema7Label=Label(dbadd,textvariable=schema7l)
    schema7Label.place(x = 20, y = 260, height=30)
    schema7Label.configure(font=gdbFont)
    schema7l.set("Enter "+myschema[6]+':')

    descriptor7=StringVar()
    dvde7=Entry(dbadd,textvariable=descriptor7, width=60)
    dvde7.place(x = 300, y = 260, width=370, height=30)
    dvde7.configure(font=gdbFont)

    schema8l=StringVar()
    schema8Label=Label(dbadd,textvariable=schema8l)
    schema8Label.place(x = 20, y = 300, height=30)
    schema8Label.configure(font=gdbFont)
    schema8l.set("Enter "+myschema[7]+':')

    descriptor8=StringVar()
    dvde8=Entry(dbadd,textvariable=descriptor8, width=60)
    dvde8.place(x = 300, y = 300, width=370, height=30)
    dvde8.configure(font=gdbFont)

    if IsSelection:
        #put the original descriptor values in the global
        value=dbListBox.get(dbListBox.curselection())
        descriptor1.set(value[0])
        descriptor2.set(value[1])
        descriptor3.set(value[2])
        descriptor4.set(value[3])
        descriptor5.set(value[4])
        descriptor6.set(value[5])
        descriptor7.set(value[6])
        descriptor8.set(value[7])

    def calltodb(routinenum):
        descList = []
        descList.append(descriptor1.get())
        descList.append(descriptor2.get())
        descList.append(descriptor3.get())
        descList.append(descriptor4.get())
        descList.append(descriptor5.get())
        descList.append(descriptor6.get())
        descList.append(descriptor7.get())
        descList.append(descriptor8.get())
        desctuple = tuple(descList)
        if routinenum == 1:
            sql.insertrow(desctuple)
            ms.dbview(dbListBox,stat2,sql)
        elif routinenum == 2:
            sql.updaterow(desctuple, value)
        return

    b1=Button(dbadd, text="Add Entry", command = lambda : calltodb(1))
    b1.place(x = 370, y = 340, width=100, height=30)   

    if IsSelection:   
        b3=Button(dbadd, text="Update Entry", command = lambda : calltodb(2))
        b3.place(x = 470, y = 340, width=100, height=30) 
    
    b4=Button(dbadd, text="Exit", command=dbadd.destroy)
    b4.place(x = 590, y = 340, width=80, height=30) 
    
    dbadd.mainloop()
    return
