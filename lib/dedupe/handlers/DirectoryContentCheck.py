import fnmatch
import os

import ddexceptions as DDE
import ddpreferences as DDPREF

DCC_prefs = {
    "exclusion_names" : {
        "dir": [".git", ".svn"],
        "file": ["*.aup"],
    }
}

DDPREF.setDefaultPreferences("config/encounters", "DirectoryContentCheck", DCC_prefs)
DCC_prefs = DDPREF.getPreference("config/encounters/DirectoryContentCheck")

def __verify(target_item, exclusions, check_function):
    contents = target_item.getContents()

    for pat in exclusions:
        matched_items = fnmatch.filter(contents, pat)
        for item in matched_items:
            if check_function("%s%s%s" % (target_item.getFullPath(), os.path.sep, item)):
                raise ProcessorSkipException("<%s> found prevents directory <%s> from being processed." %(base_name, os.path.dirname(item) ) )

def process(target_item):
    global DCC_prefs

    __verify(target_item, DCC_prefs["exclusion_names"]["dir"], os.path.isdir)
    __verify(target_item, DCC_prefs["exclusion_names"]["file"], os.path.isfile)
