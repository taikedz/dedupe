import importlib

import ddpreferences as DDPREF

__PREFS = {
    "type" : "sqlite",
    "name" : "DedupeDatabase"
}

DDPREF.setDefaultPref("config/engine/database", __PREFS)
dbengine_prefs = DDPREF.getPreference("config/engine/database")

__database_module = importlib.import_module("databases.%s" % chosen_dbengine["type"])
__database_connection = None

def getDatabaseConnection(database_name=None):
    global __database_connection
    if not database_name:
        database_name = dbengine_prefs["name"]

    if not __database_connection:
        __database_connection = DedupeDatabase(database_name)

    return __database_connection

class DedupeDatabase:
    def __init__(self, database_name):
        global __database_module
        self.__connector = __database_module.open_database(database_name)

    def registerParentPath(self, path):
        pass

    def registerFilePath(self, path):
        pass

    def registerFileIdentity(self, path):
        pass

    def registerMeta(self, keyname, value):
        pass

    def getMetaEntries(self):
        pass

    def getFileIdentity(self, identity_keys):
        """
        identity_keys is a dictionary with the keys "byte_size", "small_hash", "full_hash"
        """
        pass
