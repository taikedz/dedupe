import fnmatch
import os

import ddexceptions as DDE
import ddpreferences as DDPREF

DCC_prefs = {
    "dir": [".git", ".svn"],
    "file": ["*.aup"],
}

DDPREF.setDefaultPreferences("config/encounters/DirectoryContentCheck", DCC_prefs)
DCC_prefs = DDPREF.getPreference("config/encounters/DirectoryContentCheck")

def __verify(target_item, exclusions, check_function):
    contents = target_item.getContents()
    directory_path = target_item.getFullPath()

    for pat in exclusions:
        matched_items = fnmatch.filter(contents, pat)
        for item in matched_items:
            if check_function("%s%s%s" % (target_item.getFullPath(), os.path.sep, item)):
                raise DDE.ProcessorSkipException("DirectoryContentCheck: <%s> found prevents directory <%s> from being processed." %(item, directory_path ) )

def process(target_item):
    global DCC_prefs

    __verify(target_item, DCC_prefs["dir"], os.path.isdir)
    __verify(target_item, DCC_prefs["file"], os.path.isfile)
