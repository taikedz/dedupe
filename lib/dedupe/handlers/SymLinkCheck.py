import ddexceptions as DDE
import ddpreferences as DDPREF

SLC_prefs = {
    "allow_symlinks" : False
}

DDPREF.setDefaultPreferences("config/encounters/SymLinkCheck", SLC_prefs)
SLC_prefs = DDPREF.getPreference("config/encounters/SymLinkCheck")

def process(current_item):
    if SLC_prefs["allow_symlinks"] == False and current_item.islink():
        raise DDE.ProcessorSkipException("SymLinkCheck: Skip <%s>" %(current_item))
