import fnmatch
import os

import ddexceptions as DDE
import ddpreferences as DDPREF

IC_prefs = {
    "exclusion_names" : {
        "dir": ["__pycache__",],
        "file": ["*.pyc"],
    }
}

DDPREF.setDefaultPreferences("config/encounters/IgnoreCheck", IC_prefs)
IC_prefs = DDPREF.getPreference("config/encounters/IgnoreCheck")

def __verify(target_item, patterns, checkfunction):
    item_name = target_item.getName()
    for pat in patterns:
        if fnmatch.fnmatch(item_name, pat) and checkfunction(target_item.getFullPath() ):
            raise  DDE.ProcessorSkipException("IgnoreCheck: <%s> excluded <%s>" % (pat, item_name))

def process(target_item):
    __verify(target_item, IC_prefs["dir"], os.path.isdir)
    __verify(target_item, IC_prefs["file"], os.path.isfile)
