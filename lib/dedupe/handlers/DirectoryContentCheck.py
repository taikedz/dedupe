import fnmatch
import os

import ddexceptions as DDE
import ddpreferences as DDPREF

__setup_done = False

DCC_prefs = {
    "exclusion_names" : {
        "dir": [".git", ".svn"],
        "file": ["*.aup"],
    }
}

DDPREF.setDefaultPreferences("config/encounters", "DirectoryContentCheck", DCC_prefs)

def __doSetup():
    global __setup_done
    global DCC_prefs

    if __setup_done:
        return

    DCC_prefs = DDPREF.getPreference("DirectoryContentCheck")

def __verify(target_item, exclusions, check_function):
    contents = target_item.getContents()

    for pat in exclusions:
        matched_items = fnmatch.filter(contents, pat)
        for item in matched_items:
            if check_function("%s%s%s" % (target_item.getFullPath(), os.path.sep, item)):
                raise ProcessorSkipException("<%s> found prevents directory <%s> from being processed." %(base_name, os.path.dirname(item) ) )

def process(target_item):
    global DCC_prefs

    # We do not want this to be done prematurely, so here is best for now...
    __doSetup()

    __verify(target_item, DCC_prefs["exclusion_names"]["dir"], os.path.isdir)
    __verify(target_item, DCC_prefs["exclusion_names"]["file"], os.path.isfile)
