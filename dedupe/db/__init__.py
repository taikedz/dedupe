""" Get the database API implementation
"""

from dedupe.db.api_generic import DbApiGeneric
from dedupe.db.api_sqlite import SQLiteApi

__API = None


def get_database(*args) -> DbApiGeneric:
    """
    """
    global __API

    if __API is None:
        __API = SQLiteApi(*args)

    return __API
