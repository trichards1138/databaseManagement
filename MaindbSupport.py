#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database keeper: Is an app to organize your DVD's and CD's (or any other hobby
set) and keep track of them in case you are looking to buy a new DVD and don't 
remember if you already have it (or a tool or cloth swatch :) etc) either stand-alone 
or contained within a movie or music collection.

MaindbSupport contains the directly called routines from the main buttons and Listbox.
This file contains routines that only call other routines (in the classes)

Copyright 2020 by Perfection Quest Software
"""
from tkinter import *
from tkinter import messagebox
import dbFileSupport as fsup
import sqliteSupport as sqll
import getINIinfo as gini
import AddRow as ar
import ntpath
import os

# Will eventually go away
def donothing():
    return

# Routine to display all of the rows in the selected database table into
# the main Listbox for viewing.  Also updates the status bar
def dbview(dvdListBox,status2, sql):
    rows = []
    # as the number of rows increases, we want to decrease the number of spaces so 
    # they take the same space.  This keeps our columns aligned
    spacecnt = ["    ", "   ", "  ", " "]
    # Just a string of spaces so we can add an arbitrary number into an entry
    addspace = "                                                              "
    # The alloted number of characters for each column
    alloted = [20,20,8,15,15,15,15,15]
    # Call the database class to get the rows from the table
    rows = sql.get_rows()
    # Empty the Listbox
    dvdListBox.delete(0, END)
    liststring = ""
    currow = 1
    curcol = 0
    # iterate through the rows and add each into the listbox
    for items in rows:
        rownum = str(currow)    
        # Add the rownum onto the front end of the entry
        # add spaces to ensure "1    " ~ "1000 "
        liststring = rownum + spacecnt[len(rownum)]
        for tupleitems in items:
            # see if the len of the items is greater than the alloted len
            if len(tupleitems) > alloted[curcol]:
                # If items len is greater, only add alloted num of characters
                addstring = tupleitems[0:alloted[curcol]]
            else:
                # else add the item and spaces to align the columns
                addstring = tupleitems + addspace[0:alloted[curcol]-len(tupleitems)]
            liststring = liststring  + addstring 
            curcol += 1
        #add it in
        dvdListBox.insert(END, liststring)
        currow += 1
        curcol = 0
    # Update the number of entries in the status bar
    status2.set( "Number of Entries: {}".format(dvdListBox.size()))
    return

# Open a new database file
def Newdbfile(dvd_List,stat1,stat2,sql,fs,deleteprevmenu):
    newfilename = fs.Newdbfile()    # call the file class function
    oldfilename = sql.sqldbfname
    # is it the same file as already open
    if fs.compare_files(oldfilename, newfilename):
        messagebox.showwarning(title="File Open Warning", message=f"{newfilename} is already open")
        return
    if newfilename == "":
        return    
    else:
        # If not, close the current connection
        sql.close_conn()
        # open the new file in the database class functions
        if sql.dbconnect(newfilename):
            # update the status bar with the new filename
            stat1.set("DataBase File:  {}".format(ntpath.basename(newfilename)))
            # Since it is a new file, the user must create a new database table and schema
            # Notify them of this requirement
            messagebox.showinfo(title="Create Table Info", 
                message="File Created, select 'File Tables' -> 'Create New Table' to create a Database Table (With Schema)")
            # If there was a currently opened file, the current entries in the menu must be deleted
            deleteprevmenu()
        else:
            # Got an error trying to open the file
            messagebox.showinfo(title="Open File Info", message="Could not open New db file")
            sql.dbconect(oldfilename)
    return 

# Open an existing database file
def Opendbfile(dvd_List,stat1,stat2,sql,fs,addtablemenu,deleteprevmenu):
    newfilename = fs.Opendbfile()
    oldfilename = sql.sqldbfname
    if newfilename == "" or fs.compare_files(oldfilename, newfilename):
        messagebox.showwarning(title="File Open Warning", message=f"{newfilename} is already open")
        return
    else:
        # It's a different file, so close the current connection
        sql.close_conn()
        # Open the newly opened database file
        if sql.dbconnect(newfilename):
            sql.dbtablelist()   # Get the list of database tables in the file
            sql.table = sql.tablelist[0]    # set the current table to the first entry
            sql.getschema()     # Get the schema for the current table
            deleteprevmenu()    # Delete the entries from the previous file from the menu
            addtablemenu(sql,fs, True)  # This adds the table list to the menu
            # Update the status bar and load the Listbox with the selected table
            stat1.set("DataBase File:  {}".format(ntpath.basename(newfilename)))
            dbview(dvd_List, stat2, sql)
        else:
            messagebox.showinfo(title="Open File Info", message="Could not open db file")
            sql.dbconect(oldfilename)
    return 
 
# Save the table displayed in the listbox into a new file (existing or new)
def SaveAsdbfile(sql,fs):
    # Go get the new file name
    newfilename = fs.SaveAsdbfile()
    # Ensure it is not the same
    if fs.compare_files(sql.sqldbfname, newfilename):
        return
    else:
        oldfilename = sql.sqldbfname    # Save the current file name
        content = sql.get_rows()        # Get all of the rows from the db table
        sql.close_conn()                # close the current file
        if sql.dbconnect(newfilename):  # Try opening the new file
            sql.dbcreatetable()         # If the table doesn't exist in new file...create it
            sql.put_rows(content)       # if successful, put the rows into new file
        else:
            # Couldn't open the new file for some readon
            messagebox.showerror(title="DB SaveAs Error", 
                    message="Could not Open db file Entered")
        sql.close_conn()            # Information transfered (or an error occured)
        sql.dbconnect(oldfilename)  # Reopen previous file.
    return

# Search the database based on the parameters (entered from the combo boxes and entries)
# Then the entries found are displayed on the listbox
def search(dvd_List,stat2,descr1,descr2,descr3,descr4,header1,header2,header3,header4,sql):
    rows = []
    # same as with dbview...need to keep the columns aligned
    spacecnt = ["    ", "   ", "  ", " "]
    alloted = [20,20,8,15,15,15,15,15]   
    addspace = "                                                              "
    defaultschema = f"{sql.schema[0]}"    # set first schema entry as default search schema entry
    # Set up for database search
    schemaListi=[header1, header2, header3, header4]
    # If a search entry is left blank, fill it with default search descriptor
    schemaList = [ val if val != "" else defaultschema for val in schemaListi]
    # search descruptors are taken from user in entries on main window
    descriptorList=[descr1, descr2, descr3, descr4]
    # tupleize the data for the database class functions
    schematuple = tuple(schemaList)
    descptuple = tuple(descriptorList)
    # Search the database
    rows = sql.searchrows(schematuple, descptuple)
    dvd_List.delete(0, END)
    liststring = ""
    currow = 1
    curcol = 0
    # Display the resulting rows the same as in dbview 
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

# Delete a row entry in the Listbox and database table
def delete(dvd_List,stat2,sql):
    rowselected = dvd_List.curselection()[0] 
    # Make sure the user wants to delete the entry
    ynMsgBox = messagebox.askquestion ('Selection Delete','Are you sure you want to delete the entry',icon = 'warning')
    if ynMsgBox == 'no':
        return
    # If yes, delete it from the database table
    rowcontent = sql.rows[rowselected]
    sql.deleterow(rowcontent)
    # dbview will refill the listbox without the deleted entry
    dbview(dvd_List, stat2, sql)
    return

# Fills the main window comboboxes with the schema for the currently selected database table
def fillinCombo(comboname, fillList, headervar, decriptorvar):
    # The "values" are the List of entries
    comboname['values'] = fillList
    # Select none of the entries so the inital combo box text is empty (until user selects)
    comboname.current()
    headervar.set("")
    decriptorvar.set("")
    return

# get and set a new db file, table, and item parameter set for the new db
# This function gets a new db from the ini structure (not a file)
def selectnewinidb(dvd_List,stat1,stat2,sql,fs,combolist,secnum):
    value = []
    result = True
    # secnum is the menu selector
    secn = secnum.get()
    # get the data for the new ini section selected
    dbtable = fs.items[secn][1]
    Path = fs.items[secn][2]
    dbname = fs.items[secn][3]
    dbfname = Path + dbname
    if dbfname != sql.sqldbfname:
        # the new section file is different, prepare to open the new file
        sql.close_conn()
        result = sql.dbconnect(dbfname)
        if not result:
            messagebox.showerror(title="db File Error", message=f"Could not Open the db File {dbfname}")
    # new database table name
    sql.table = dbtable
    # entry 4 - 12 contain the table schema needed to manage the entries
    valnum = 4
    while valnum < 12:
        value.append(fs.items[secn][valnum])
        valnum += 1
    # tupleize the schema
    sql.schema = tuple(value)
    if not result:
        return False
    # Create the table if it does not exist
    # does nothing if the table already exists
    sql.dbcreatetable()
    schemaList = []
    scount = 0
    # create a list from the schema tuple for the combos
    while scount < 8:
        schemaList.append(sql.schema[scount])
        scount += 1
    fillinCombo(combolist[0], schemaList, combolist[1], combolist[2])
    fillinCombo(combolist[3], schemaList, combolist[4], combolist[5])
    fillinCombo(combolist[6], schemaList, combolist[7], combolist[8])
    fillinCombo(combolist[9], schemaList, combolist[10], combolist[11])
    # Now we can display the database rows from the table
    dbview(dvd_List, stat2, sql)
    # Update the status bar (file name) (number of entries updated in dbview)
    stat1.set( f"DataBase File:  {dbname}")
    return 

# get and set a new db file, table, and item parameter set for the new db
# This function gets a new db from the file structure (not the INI)
def selectnewfiledb(dvd_List,stat1,stat2,sql,fs,combolist,secnum):
    
    result = True
    # is the filename different than the current?
    if sql.sqldbfname != fs.filedbname:
        # if yes, close the current and open the new
        sql.close_conn()
        result = sql.dbconnect(fs.filedbname)
        if not result:
            messagebox.showerror(title="db File Error", message=f"Could not Open the db File {sql.sqldbfname}")
 
    # Section number from the menu
    secn = secnum.get() - 2
    # Get the new table and schema data from the new selection
    sql.table = sql.tablelist[secn]
    sql.getschema()
    schemaList = []
    scount = 0
    while scount < 8:
        schemaList.append(sql.schema[scount])
        scount += 1
    # Fill in the new schema to the combo boxes
    fillinCombo(combolist[0], schemaList, combolist[1], combolist[2])
    fillinCombo(combolist[3], schemaList, combolist[4], combolist[5])
    fillinCombo(combolist[6], schemaList, combolist[7], combolist[8])
    fillinCombo(combolist[9], schemaList, combolist[10], combolist[11])
    # display the data from the new table in the listbox and status bar
    dbview(dvd_List, stat2, sql)
    stat1.set("DataBase File:  {}".format(ntpath.basename(sql.sqldbfname)))
    return 

def AboutBox():     # Put up the About box for the user
    messagebox.showinfo(title="About Database Management",
    message="Simple Database Management software for building Minder databases \
for your mobile devices. When out and about and looking at additions to your collection, \
you will know if you have an item already or not.\n\nCopyright 2020 - Perfection Quest Software")
    return

def fclose(dvdListBox, stat1, stat2, sql):
    sql.close_conn()
    sql.sqldbfname = ""
    stat1.set( "DataBase File:  ")
    stat2.set( "Number of Entries: 0")
    dvdListBox.delete(0, END)
    return
    