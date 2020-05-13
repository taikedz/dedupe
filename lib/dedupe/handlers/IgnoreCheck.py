import fnmatch
import os

import ddexceptions as DDE
import ddpreferences as DDPREF
import ddlog

log = ddlog.getLogger()

IC_prefs = {
    "dir": ["__pycache__",],
    "file": ["*.pyc"],
}

DDPREF.setDefaultPreferences("config/encounters/IgnoreCheck", IC_prefs)
IC_prefs = DDPREF.getPreference("config/encounters/IgnoreCheck")

def __verify(target_item, patterns, checkfunction):
    item_name = target_item.getName()
    log.debug("Checking[%s] -- %s : %s"%(item_name, str(checkfunction) , checkfunction(target_item.getFullPath())) )
    for pat in patterns:
        log.debug("  --> Pat[%s]" % (pat))
        if fnmatch.fnmatch(item_name, pat) and checkfunction(target_item.getFullPath() ):
            raise  DDE.ProcessorSkipException("IgnoreCheck: <%s> excluded <%s>" % (pat, item_name))

def process(target_item):
    __verify(target_item, IC_prefs["dir"], os.path.isdir)
    __verify(target_item, IC_prefs["file"], os.path.isfile)
