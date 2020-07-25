#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database keeper: Is an app to organize your DVD's and CD's (or any other hobby
set) and keep track of them in case you are looking to buy a new DVD and don't 
remember if you already have it (or a tool or cloth swatch :) etc) either stand-alone 
or contained within a movie or music collection.

File Support includes finding the directory and filename of the selected 
database and creating a new db if the user desires.

Copyright 2020 by Perfection Quest Software
"""
from tkinter import *
from tkinter import messagebox
import configparser
import tkinter.filedialog as fd
from tkinter.font import Font
import ntpath
import sys
import os

class dbfileSupport:    # Database file support routines class

    # When we initalize the configparser to read in the ini file when we
    # open the class. 
    def __init__(self):
        self.conf = configparser.ConfigParser()  #class to read our config file 
        result = self.conf.read("db.ini")        #function to open the INI file
        if result == []:                    #read opens the file and returns list
            self.valid_config = False            #if the returned list is empty
        else:                               #return False
            self.valid_config = True             #else we found and opened ini file
        return        
    
    # Read the INI file and parse out the db file and table information for each section
    def get_items(self):
        self.items = []
        section = []
        secnum = 1
        while True:
            # database set name
            try:
                section.append(self.conf[f"DataBase Set {secnum}"]["name"])
            except:
                #print("we excepted at" + str(secnum))
                break   # should get exception when we try to read a non-existent section
            #dbhandle is what the db is called in sqlite
            try:    #anything that can be left incomplete by user must be tested
                section.append(self.conf[f"DataBase Set {secnum}"]["dbtable"])
            except:
                break
            # path to database file
            try:
                section.append(self.conf[f"DataBase Set {secnum}"]["path"])
            except:
                break
            # database filename
            try:
                section.append(self.conf[f"DataBase Set {secnum}"]["fname"])
            except:
                break
            # item descriptors
            try:
                for key in self.conf[f"Item Set {secnum}"]:
                    section.append(self.conf[f"Item Set {secnum}"][key])
            except:
                break
            self.items.append(section)
            secnum += 1
            section = []
        self.numsec = secnum - 1
        self.cursec = 0
        return

    # Check whether a file exists
    def filenotExists(self,fname):
        try:
            f = open(fname)   #try to open the file
            f.close()         #if it did open, immediataly close it
        except FileNotFoundError:
            return True       #if the file was not found or an IO error was
        except IOError:     #detected, return True (it does exist)
            return True
        return False        #we found and opened the file...return False


    # Compare two files and see if they are the same.  don't need to open
    # a new file if it is the same as the one already open.
    def compare_files(self, fname1, fname2):
        cfname1 = ntpath.basename(fname1)
        cfname2 = ntpath.basename(fname2)
        if cfname1 == cfname2:
            cpath1 = ntpath.dirname(fname1)
            cpath2 = ntpath.dirname(fname2)
            if cpath1 == cpath2:
                return True         #return true if path and filenames match

        return False
    
    # find a new database file to open.  This must be an existing file
    def Opendbfile(self):
        dbfilename = fd.askopenfilename(initialdir=os.getcwd(),title = "Open DataBase file",
            filetypes = (("db Files","*.db"),("all files","*.*")))
        if dbfilename == ():    # Gives an empty tuple if the cancel button is hit
            messagebox.showerror(title="db File Entry Error", 
                message = "No File Name Was Entered!")
            return ""
        self.filedbname = dbfilename
        return dbfilename
   
    # Open a file to save the existing database to.  This can be a new file or an existing one
    def SaveAsdbfile(self):
        dbfilename =  fd.asksaveasfilename(initialdir=os.getcwd(),title = "Save to New DataBase file",
            filetypes = (("db Files","*.db"),("all files","*.*")))
        if dbfilename == ():
            messagebox.showerror(title="db File Entry Error", 
                    message = "No File Name Was Entered!")
            return ""
        return dbfilename

    # Open and create a new file (with inital database table and schema)
    def Newdbfile(self):
        dbfilename =  fd.asksaveasfilename(initialdir=os.getcwd(),title = "Open New DataBase file",
            filetypes = (("db Files","*.db"),("all files","*.*")))
        if dbfilename == ():
            messagebox.showerror(title="db File Entry Error", 
                message = "No File Name Was Entered!")
            return ""
        self.filedbname = dbfilename
        return dbfilename

    # If you create a new database, you can save a bare database section in your
    # ini file.  You will probably want to add some comments to it in an editor
    def addsec2ini(self, iniList):
        name = iniList[0]   #iniList is set in the Get INI info dialog (select in menu)
        table = iniList[1]
        path = iniList[2]
        fname = iniList[3]
        schema = iniList[4]
        numsets = iniList[5]

        # open a new config parser to contain the updates
        config_update = configparser.ConfigParser()
            
        # First section is the Database Set - (name of entry, database table name,
        # Path, and filename)
        dsl = f"DataBase Set {str(numsets+1)}"
        config_update.add_section(dsl)
        config_update.set(dsl, 'name', name)
        config_update.set(dsl, 'dbtable', table)
        config_update.set(dsl, 'path', path)
        config_update.set(dsl, 'fname', fname)

        # Second section is the database schema for the above table
        isl = f"Item Set {str(numsets+1)}"
        config_update.add_section(isl)
        config_update.set(isl, 'value1', schema[0])
        config_update.set(isl, 'value2', schema[1])
        config_update.set(isl, 'value3', schema[2])
        config_update.set(isl, 'value4', schema[3])
        config_update.set(isl, 'value5', schema[4])
        config_update.set(isl, 'value6', schema[5])
        config_update.set(isl, 'value7', schema[6])
        config_update.set(isl, 'value8', schema[7])
        try:
            # Open the ini file
            inifile = open("./db.ini", "a")
        except:
            messagebox.showerror(title="File Error", 
                   message="Cannot open Config file!\nConfig not Written!")
            return False
        # Write the new sections
        config_update.write(inifile, space_around_delimiters=False)
        # close the ini file
        inifile.close()
        # Let user know we are done and successful
        messagebox.showinfo(title="INI File", message="INI File Updated")
        # Now update some bookkeeping and put it into the "items" so we 
        # know about them for the rest of the session
        self.numsec = numsets + 1
        iniList.pop(len(iniList)-1)
        newsection = []
        item = 0
        #put in name, table, path, and fname
        while item < 4:
            newsection.append(iniList[item])
            item +=1
        #put in the db schema (8 items)
        item = 0
        while item < 8:
            newsection.append(iniList[4][item])
            item += 1
        # items is a list of ini sections
        self.items.append(newsection)
        return True

    # clean up and delete ourselves - currently not called
    def __del__(self):
        del self.conf
        del self
        return