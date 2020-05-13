import fnmatch
import os

import ddexceptions as DDE
import ddpreferences as DDPREF

# Deliberately empty sets
# We should not be deleting anything by default, leave this to user's prefs
DC_prefs = {
    "exclusion_names" : {
        "dir": [],
        "file": [],
    }
}

DDPREF.setDefaultPreferences("config/encounters/IgnoreCheck", DC_prefs)
DC_prefs = DDPREF.getPreference("config/encounters/IgnoreCheck")

def __verify(target_item, patterns, checkfunction):
    item_name = target_item.getName()
    for pat in patterns:
        full_path = target_item.getFullPath() 
        if fnmatch.fnmatch(item_name, pat) and checkfunction(full_path):
            os.rm(full_path )
            raise DDE.ProcessorSkipException("DeleteCheck: <%s> removed <%s>" % (pat, full_path))

def process(target_item):
    __verify(target_item, DC_prefs["dir"], os.path.isdir)
    __verify(target_item, DC_prefs["file"], os.path.isfile)

