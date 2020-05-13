import ddexceptions as DDE
import ddpreferences as DDPREF

__setup_done = False

SLC_prefs = {
    "allow_symlinks" : False
}

DDPREF.setDefaultPreferences("config/encounters", "SymLinkCheck", SLC_prefs)

def __doSetup():
    global __setup_done
    global SLC_prefs

    if __setup_done:
        return

    SLC_prefs = DDPREF.getPreference("SymLinkCheck")

def process(current_item):
    _doSetup()
    if SLC_prefs["allow_symlinks"] == False and current_item.islink():
        raise ProcessorSkipException("Skip %s" %(current_item))
