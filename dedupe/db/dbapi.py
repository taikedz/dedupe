from typing import Tuple

# abstract away the database
from dedupe.db import api_sqlite as DBAPI

def open_database(dbpath):
    DBAPI.open()


def ensure_table(table_name:str, tabledef:dict):
    raise


def register(path:str, size:int, short_hash:str, full_hash:str) -> None:
    raise


def lookup_size(size:int) -> Tuple[str,str]:
    raise


def lookup_hash_short(short_hash:str) -> Tuple[str,str]:
    raise


def lookup_hash_full(full_hash:str) -> Tuple[str,str]:
    raise


def get_duplicates_hashes():
    raise
