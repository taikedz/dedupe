import ddexceptions as DDE

"""
Preferences loader - supply a file in YAML format to extract it
"""

__preferences_data = {}
__preferences_loaded = False

__prefs_locked_message = "Preferences have already been loaded, and are now locked. Implementation error."

def setDefaultPreferences(prefs_name, prefs_object):
    """ Before loading preferences, specify the defaults

    Raises ddexceptions.PreferencesLocked if called after loadPreferences()
    """
    if __preferences_loaded:
        raise DDE.PreferencesLocked(__prefs_locked_message)
    
    __preferences_data[prefs_name] = prefs_object

def loadPreferences(prefs_file):
    """ Load a preferences file.

    This function MUST be called after any modules call setDefaultPreferences()

    Raises ddexceptions.PreferencesLocked if called more than once.
    """
    global __preferences_loaded
    if __preferences_loaded:
        raise DDE.PreferencesLocked(__prefs_locked_message)
    __preferences_loaded = True
    
    raise DDE.NotImplemented("loadPreferences() not implemented in ddpreferences.py")
    # implementation note - must implement prefs merging.
    # load existing prefs onto the default prefs
    # anything not specified in file still provided by prefs
    # and then can allow multiple loadPreferences() calls

def getPreference(pref_name):
    return __preferences_data[pref_name]
