""" Get the database API implementation
"""

from dedupe.db.api_generic import DbApiGeneric, DedupeDatabaseError
from dedupe.db.api_sqlite import SQLiteApi

__API = None

def get_database() -> DbApiGeneric:
    return __API


def open_database(db_type, *args, **kwargs) -> DbApiGeneric:
    """ Open a databse connection, and return its 
    """
    global __API

    NewDatabase = None
    if db_type == "sqlite3":
        NewDatabase = SQLiteApi

    if __API is None:
        __API = NewDatabase(*args, **kwargs)
    else:
        raise DedupeDatabaseError("Already opened.")
    
    return __API
