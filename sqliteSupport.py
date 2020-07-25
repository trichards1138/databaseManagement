#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database keeper: Is an app to organize your DVD's and CD's (or any other hobby
set) and keep track of them in case you are looking to buy a new DVD and don't 
remember if you already have it (or a tool or cloth swatch :) etc) either stand-alone 
or contained within a movie or music collection.

Sqlite support interfaces with the database after it is opened.  Record 
retrieval and addition is supported here.

Copyright 2020 by Perfection Quest Software
"""
import sqlite3

class dbsupport:    #database support class

    # some class global attributes
    table = "dvd"
    schema = ("Title", "Lead_Star", "Release_Year", "Genre", "Collection", "Location", "Rating", "Misc")
    sqldbfname = ""
    conn = None

    def __init__(self):    
        return

    # Connect to a new database file.  Should call close first
    def dbconnect(self, fname): 
        self.sqldbfname = fname
        try:
            self.conn=sqlite3.connect(self.sqldbfname)
        except:
            return False
        self.cur=self.conn.cursor()
        return True
   
    # Create an database table with schema (a descriptor values) if it doesn't exist
    def dbcreatetable(self):
        try:
            self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table} ({self.schema[0]},{self.schema[1]},{self.schema[2]}, \
                {self.schema[3]},{self.schema[4]},{self.schema[5]},{self.schema[6]},{self.schema[7]})")
            self.conn.commit()
        except:
            return False
        return True

    # Get the schema of the table just opened (used when opening a new file)
    def getschema(self):
        schemalist = []
        self.cur.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{self.table}')")
        self.conn.commit()
        self.tableschema=self.cur.fetchall()
        for value in self.tableschema:
            schemalist.append(value[0])
        self.schema = tuple(schemalist)
        return self.schema

    # Get a list of database tables in the file just opened to display in the menu
    def dbtablelist(self):
        self.tablelist = []
        self.cur.execute("SELECT name FROM \
        (SELECT * FROM sqlite_master UNION ALL SELECT * FROM sqlite_temp_master) \
        WHERE type='table' \
        ORDER BY name")
        self.conn.commit()
        self.tablelist=self.cur.fetchall()
        self.tablelist = [value[0] for value in self.tablelist]
        return

    #insert the row contents (rowcont) into the table selected
    def insertrow(self, rowcont):
        self.cur.execute(f"INSERT INTO {self.table} VALUES (?,?,?,?,?,?,?,?)",rowcont)
        self.conn.commit()
        return

    #Select a db table and search for the row entry(s) that match the 4 provided search parameters (descriptor values)
    def searchrows(self, value, rowcont):
        self.cur.execute(f"SELECT * FROM {self.table} WHERE {value[0]}=? OR {value[1]}=? OR {value[2]}=? OR {value[3]}=?",
                 rowcont)
        self.rows=self.cur.fetchall()
        return self.rows
    
    # delete the db row from the db table selected that matches the parameters in rowcont
    def deleterow(self, rowcont):
        self.cur.execute(f"DELETE FROM {self.table} WHERE {self.schema[0]}=? AND {self.schema[1]}=? AND {self.schema[2]}=? AND \
            {self.schema[3]}=? AND {self.schema[4]}=? AND {self.schema[5]}=? AND {self.schema[6]}=? AND {self.schema[7]}=?",
                rowcont)
        self.conn.commit()
        return

    # update the db row in the db table that matches (new_rowcont or new row content is the new data for the row)
    def updaterow(self, new_rowcont, rowcont):
        self.cur.execute(f"UPDATE {self.table} SET {self.schema[0]}=?, {self.schema[1]}=?, {self.schema[2]}=?, {self.schema[3]}=?, \
            {self.schema[4]}=?, {self.schema[5]}=?, {self.schema[6]}=?, {self.schema[7]}=? WHERE {self.schema[0]}=? AND {self.schema[1]}=?  \
            AND {self.schema[2]}=? AND {self.schema[3]}=? AND {self.schema[4]}=? AND {self.schema[5]}=? AND {self.schema[6]}=? AND  \
            {self.schema[7]}=?", new_rowcont, rowcont)
        self.conn.commit()
        return
    
    # Get all of the row content from the seleted db table
    def get_rows(self):
        self.cur.execute(f"SELECT * FROM {self.table}")
        self.rows=self.cur.fetchall()
        return self.rows

    # Put a series of row content into the selected table
    def put_rows(self,rowcont):
        for values in rowcont:
            self.cur.execute(f"INSERT INTO {self.table} VALUES (?,?,?,?,?,?,?,?)",(values))
        self.conn.commit()
        return

    # close the connection (use if you are opening a new file)
    def close_conn(self):
        if self.conn:
            self.conn.close()
        return

    # We are done...destroy the class.  This is done automatically so this is not called.
    def __del__(self):
        del self
        return
