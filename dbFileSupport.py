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
from tkinter import messagebox
import configparser
import tkinter.filedialog as fd
from tkinter.font import Font
import ntpath
import sys
import os

class dbfileSupport:

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

    def filenotExists(self,fname):
        try:
            f = open(fname)   #try to open the file
            f.close()         #if it did open, immediataly close it
        except FileNotFoundError:
            return True       #if the file was not found or an IO error was
        except IOError:     #detected, return True (it does exist)
            return True
        return False        #we found and opened the file...return False


    def compare_files(self, fname1, fname2):
        cfname1 = ntpath.basename(fname1)
        cfname2 = ntpath.basename(fname2)
        if cfname1 == cfname2:
            cpath1 = ntpath.dirname(fname1)
            cpath2 = ntpath.dirname(fname2)
            if cpath1 == cpath2:
                return True         #return true if path and filenames match

        return False
    
    def Opendbfile(self):
        dbfilename = fd.askopenfilename(initialdir=os.getcwd(),title = "Open DataBase file",
            filetypes = (("db Files","*.db"),("all files","*.*")))
        if dbfilename == ():
            messagebox.showerror(title="db File Entry Error", 
                message = "No File Name Was Entered!")
            return ""
        self.filedbname = dbfilename
        return dbfilename
   
    def SaveAsdbfile(self):
        dbfilename =  fd.asksaveasfilename(initialdir=os.getcwd(),title = "Save to New DataBase file",
            filetypes = (("db Files","*.db"),("all files","*.*")))
        if dbfilename == ():
            messagebox.showerror(title="db File Entry Error", 
                    message = "No File Name Was Entered!")
            return ""
        return dbfilename

    def Newdbfile(self):
        dbfilename =  fd.asksaveasfilename(initialdir=os.getcwd(),title = "Open New DataBase file",
            filetypes = (("db Files","*.db"),("all files","*.*")))
        if dbfilename == ():
            messagebox.showerror(title="db File Entry Error", 
                message = "No File Name Was Entered!")
            return ""
        self.filedbname = dbfilename
        return dbfilename

    def addsec2ini(self, iniList):
        name = iniList[0]
        table = iniList[1]
        path = iniList[2]
        fname = iniList[3]
        schema = iniList[4]
        numsets = iniList[5]

        config_update = configparser.ConfigParser()
            
        dsl = f"DataBase Set {str(numsets+1)}"
        config_update.add_section(dsl)
        config_update.set(dsl, 'name', name)
        config_update.set(dsl, 'dbtable', table)
        config_update.set(dsl, 'path', path)
        config_update.set(dsl, 'fname', fname)

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
            inifile = open("./db.ini", "a")
        except:
            messagebox.showerror(title="File Error", 
                   message="Cannot open Config file!\nConfig not Written!")
            return False
        config_update.write(inifile, space_around_delimiters=False)
        inifile.close()
        messagebox.showinfo(title="INI File", message="INI File Updated")
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
        self.items.append(newsection)
        return True

    def __del__(self):
        del self.conf
        del self
        return