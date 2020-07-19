#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DVD keeper: Is an app to organize your DVD's and CD's and keep track of them
in case you are looking to buy a new DVD and don't remember if you already
have it either stand-alone or contained within a movie or music collection.
"""
from tkinter import *
from tkinter import messagebox
import dbFileSupport as fsup
import sqliteSupport as sqll
import getINIinfo as gini
import AddRow as ar
import ntpath
import os

def donothing():
    return

def dbview(dvdListBox,status2, sql):
    rows = []
    spacecnt = ["    ", "   ", "  ", " "]
    addspace = "                                                              "
    alloted = [20,20,8,15,15,15,15,15]
    rows = sql.get_rows()
    dvdListBox.delete(0, END)
    liststring = ""
    currow = 1
    curcol = 0
    for items in rows:
        rownum = str(currow)
        liststring = rownum + spacecnt[len(rownum)]
        for tupleitems in items:
            if len(tupleitems) > alloted[curcol]:
                addstring = tupleitems[0:alloted[curcol]]
            else:
                addstring = tupleitems + addspace[0:alloted[curcol]-len(tupleitems)]
            liststring = liststring  + addstring 
            curcol += 1
        dvdListBox.insert(END, liststring)
        currow += 1
        curcol = 0
    status2.set( "Number of Entries: {}".format(dvdListBox.size()))
    return


def Newdbfile(dvd_List,stat1,stat2,sql,fs,deleteprevmenu):
    newfilename = fs.Newdbfile()
    oldfilename = sql.sqldbfname
    if fs.compare_files(oldfilename, newfilename):
        messagebox.showwarning(title="File Open Warning", message=f"{newfilename} is already open")
        return
    if newfilename == "":
        return    
    else:
        sql.close_conn()
        if sql.dbconnect(newfilename):
            stat1.set("DataBase File:  {}".format(ntpath.basename(newfilename)))
            messagebox.showinfo(title="Create Table Info", 
                message="File Created, select 'File Tables' -> 'Create New Table' to create a Database Table (With Schema)")
            deleteprevmenu()
        else:
            messagebox.showinfo(title="Open File Info", message="Could not open New db file")
            sql.dbconect(oldfilename)
    return 

def Opendbfile(dvd_List,stat1,stat2,sql,fs,addtablemenu,deleteprevmenu):
    newfilename = fs.Opendbfile()
    oldfilename = sql.sqldbfname
    if newfilename == "" or fs.compare_files(oldfilename, newfilename):
        messagebox.showwarning(title="File Open Warning", message=f"{newfilename} is already open")
        return
    else:
        sql.close_conn()
        if sql.dbconnect(newfilename):
            sql.dbtablelist()
            sql.table = sql.tablelist[0]
            sql.getschema()
            #populate the combo boxes
            deleteprevmenu()
            addtablemenu(sql,fs, True)
            stat1.set("DataBase File:  {}".format(ntpath.basename(newfilename)))
            dbview(dvd_List, stat2, sql)
        else:
            messagebox.showinfo(title="Open File Info", message="Could not open db file")
            sql.dbconect(oldfilename)
    return 
 
def SaveAsdbfile(sql,fs):
    newfilename = fs.SaveAsdbfile()
    if fs.compare_files(sql.sqldbfname, newfilename):
        return
    else:
        oldfilename = sql.sqldbfname
        content = sql.get_rows()
        sql.close_conn()
        if sql.dbconnect(newfilename):
            sql.put_rows(content)
        else:
            messagebox.showerror(title="DB SaveAs Error", 
                    message="Could not Open db file Entered")
        sql.close_conn()
        sql.dbconnect(oldfilename)
    return

def search(dvd_List,stat2,descr1,descr2,descr3,descr4,header1,header2,header3,header4,sql):
    rows = []
    spacecnt = ["    ", "   ", "  ", " "]
    alloted = [20,20,8,15,15,15,15,15]   
    addspace = "                                                              "
    schemaListi=[header1, header2, header3, header4]
    schemaList = [ val if val != "" else "Title" for val in schemaListi]
    descriptorList=[descr1, descr2, descr3, descr4]
    schematuple = tuple(schemaList)
    descptuple = tuple(descriptorList)
    rows = sql.searchrows(schematuple, descptuple)
    dvd_List.delete(0, END)
    liststring = ""
    currow = 1
    curcol = 0
    for items in rows:
        rownum = str(currow)
        liststring = rownum + spacecnt[len(rownum)]
        for tupleitems in items:
            if len(tupleitems) > alloted[curcol]:
                addstring = tupleitems[0:alloted[curcol]]
            else:
                addstring = tupleitems + addspace[0:alloted[curcol]-len(tupleitems)]
            liststring = liststring  + addstring 
            curcol += 1
        dvd_List.insert(END, liststring)
        curcol = 0
        currow += 1
    stat2.set( "Number of Entries: {}".format(dvd_List.size()))
    return

def delete(dvd_List,stat2,sql):
    rowselected = dvd_List.curselection()[0] 
    
    ynMsgBox = messagebox.askquestion ('Selection Delete','Are you sure you want to delete the entry',icon = 'warning')
    if ynMsgBox == 'no':
        return
    
    rowcontent = sql.rows[rowselected]
    sql.deleterow(rowcontent)
    dbview(dvd_List, stat2, sql)
    return

def fillinCombo(comboname, fillList):
    comboname['values'] = fillList
    comboname.current()
    return

# get and set a new db file, table, and item parameter set for the new db
# This function gets a new db from the ini structure (not a file)
def selectnewinidb(dvd_List,stat1,stat2,sql,fs,combolist,secnum):
    value = []
    result = True
    secn = secnum.get()
    dbtable = fs.items[secn][1]
    Path = fs.items[secn][2]
    dbname = fs.items[secn][3]
    dbfname = Path + dbname
    if dbfname != sql.sqldbfname:
        sql.close_conn()
        result = sql.dbconnect(dbfname)
        if not result:
            messagebox.showerror(title="db File Error", message=f"Could not Open the db File {dbfname}")
    sql.table = dbtable
    valnum = 4
    while valnum < 12:
        value.append(fs.items[secn][valnum])
        valnum += 1
    sql.schema = tuple(value)
    if not result:
        return False
    sql.dbcreatetable()
    schemaList = []
    scount = 0
    while scount < 8:
        schemaList.append(sql.schema[scount])
        scount += 1
    fillinCombo(combolist[0], schemaList)
    fillinCombo(combolist[1], schemaList)
    fillinCombo(combolist[2], schemaList)
    fillinCombo(combolist[3], schemaList)
    dbview(dvd_List, stat2, sql)
    stat1.set( f"DataBase File:  {dbname}")
    return 

# get and set a new db file, table, and item parameter set for the new db
# This function gets a new db from the file structure (not the INI)
def selectnewfiledb(dvd_List,stat1,stat2,sql,fs,combolist,secnum):
    
    result = True
    if sql.sqldbfname != fs.filedbname:
        sql.close_conn()
        result = sql.dbconnect(fs.filedbname)
        if not result:
            messagebox.showerror(title="db File Error", message=f"Could not Open the db File {sql.sqldbfname}")
        else:
            deleteprevmenu()
    secn = secnum.get() - 2
    sql.table = sql.tablelist[secn]
    sql.getschema()
    schemaList = []
    scount = 0
    while scount < 8:
        schemaList.append(sql.schema[scount])
        scount += 1
    fillinCombo(combolist[0], schemaList)
    fillinCombo(combolist[1], schemaList)
    fillinCombo(combolist[2], schemaList)
    fillinCombo(combolist[3], schemaList)
    dbview(dvd_List, stat2, sql)
    stat1.set("DataBase File:  {}".format(ntpath.basename(sql.sqldbfname)))
    return 

    