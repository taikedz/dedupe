import os

import ddexceptions as DDE
import ddpreferences as DDPREF

__setup_done = False

DCC_prefs = {
    "exclusion_names" : {
        "dir": [".git", ".svn"],
        "file": [],
    }
}

DDPREF.setDefaultPreferences("ProjectNameCheck", DCC_prefs)

def __doSetup():
    global __setup_done
    global DCC_prefs

    if __setup_done:
        return

    DCC_prefs = DDPREF.getPreference("ProjectNameCheck")

def __verify(contents, exclusions, check_function):
    # We do not want this to be done prematurely, so here is best for now...
    __doSetup()

    for item in contents:
        base_name = os.path.basename(item)
        if base_name in exclusions and check_function(item):
            raise ProcessorSkipException("<%s> found prevents directory <%s> from being processed." %(base_name, os.path.dirname(item) ) )

def process(target_item):
    global DCC_prefs

    contents = target_item.getContents(full_paths=True)

    __verify(contents, DCC_prefs["exclusion_names"]["dir"], os.path.isdir)
    __verify(contents, DCC_prefs["exclusion_names"]["file"], os.path.isfile)
