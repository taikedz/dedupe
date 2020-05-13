import yaml
import copy

import ddlog
import ddexceptions as DDE

"""
Preferences loader - supply a file in YAML format to extract it
"""

__preferences_data = {}
__preferences_loaded = False
log = ddlog.getLogger("dedupe")

def setDefaultPreferences(preferences_path, prefs_object):
    """ After loading preferences file, specify the defaults

    Raises ddexceptions.PreferencesLocked if called before loadPreferences()

    preferences_path - a "/"-delimited string, to the section into which to add the preference data

    prefs_object - a dictionary representing the set of preferences

    Example:

        setDefaultPreferences("config/encounters/SymLinkCheck", {"allow_symlinks": False})
    """
    if not __preferences_loaded:
        raise DDE.PreferencesLocked("Preferences file must be loaded first. Implementation error.")
    
    prefs_location = __preferences_data
    preferences_sections = preferences_path.split("/")
    prefs_name = preferences_sections.pop() # Save the last name for in-place dereferencing

    log.debug("prefs_name = %s"%prefs_name)

    for section in preferences_sections:
        if section not in prefs_location.keys():
            log.debug("Create pref %s"%section)
            prefs_location[section] = {}
        prefs_location = prefs_location[section]

    if prefs_name not in prefs_location.keys():
        loaded_prefs = {}
    else:
        loaded_prefs = prefs_location[prefs_name]

    prefs_location[prefs_name] = {**prefs_object, **loaded_prefs}

    log.debug("Default preferences added. Global preferences object is now:")
    log.debug(str(__preferences_data))
    # NOTE - The loaded prefs take precedence over the defaults
    # even though the file data was loaded prior

def loadPreferences(prefs_file_path):
    """ Load a preferences file.

    This function MUST be called after any modules call setDefaultPreferences()

    Raises ddexceptions.PreferencesLocked if called more than once.
    """
    global __preferences_loaded
    global __preferences_data

    if __preferences_loaded:
        raise DDE.PreferencesLocked("File preferences have already been loaded, and are now locked. Implementation error.")
    __preferences_loaded = True

    if prefs_file_path == None:
        return

    with open(prefs_file_path, 'r') as prefs_file_fh:
        __preferences_data = yaml.load(prefs_file_fh)

def getPreference(preferences_path):
    """ Retrieve a preferences object

    preferences_path - a "/"-delimited string, to the section from which to retrieve the preference data

    Example:

        getPreference("config/encounters/SymLinkCheck")
    """
    prefs_location = __preferences_data
    for section in preferences_path.split("/"):
        if section not in prefs_location.keys():
            raise DDE.PreferenceUnkown(preferences_path)
        else:
            prefs_location = prefs_location[section]

    return copy.deepcopy(prefs_location)
