import sqlite3

__connector = None

def open_database(database_name):
    global __conector

    database_name = database_name+".sqlite"

    __connector = sqlite3.connect(database_name)

def select(where=None):
    if where != None:
        where = "WHERE "+where

    __connector.query()
