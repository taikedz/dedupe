import yaml
import copy

import ddexceptions as DDE

"""
Preferences loader - supply a file in YAML format to extract it
"""

__preferences_data = {}
__preferences_loaded = False

__prefs_locked_message = "Preferences have already been loaded, and are now locked. Implementation error."

def setDefaultPreferences(preferences_path, prefs_object):
    """ After loading preferences file, specify the defaults

    Raises ddexceptions.PreferencesLocked if called before loadPreferences()

    preferences_path - a "/"-delimited string, to the section into which to add the preference data

    prefs_object - a dictionary representing the set of preferences

    Example:

        setDefaultPreferences("config/encounters/SymLinkCheck", {"allow_symlinks": False})
    """
    if not __preferences_loaded:
        raise DDE.PreferencesLocked(__prefs_locked_message)
    
    prefs_location = __preferences_data
    for section in preferences_path.split("/"):
        if section not in __preferences_data.keys():
            __preferences_data[section] = {}
        prefs_location = __preferences_data[section]

    loaded_prefs = prefs_location
    prefs_location[prefs_name] = {**prefs_object, **loaded_prefs}
    # NOTE - The loaded prefs take precedence over the defaults
    # even though the file data was loaded prior

def loadPreferences(prefs_file):
    """ Load a preferences file.

    This function MUST be called after any modules call setDefaultPreferences()

    Raises ddexceptions.PreferencesLocked if called more than once.
    """
    global __preferences_loaded
    if __preferences_loaded:
        raise DDE.PreferencesLocked(__prefs_locked_message)
    __preferences_loaded = True

    with open(prefs_file_name, 'r') as prefs_file_fh:
        __preferences_data = yaml.load(prefs_file_fh)

def getPreference(preferences_path):
    """ Retrieve a preferences object

    preferences_path - a "/"-delimited string, to the section from which to retrieve the preference data

    Example:

        getPreference("config/encounters/SymLinkCheck")
    """
    prefs_location = __preferences_data
    for section in preferences_path.split("/"):
        if section not in __preferences_data.keys():
            __preferences_data[section] = {}
        prefs_location = __preferences_data[section]

    return copy.deepcopy(prefs_location)
