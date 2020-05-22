#!/usr/bin/env python

import ddpreferences as DDPREF
import ddargparse
import ddpaths

def parseArguments(args):
    return ddargparse.parseArguments(args)

def loadPreferences(config_path):
    if config_path == None:
        config_paths = ddpaths.resolveAll(ddpaths.global_config_paths)
        for path in config_paths:
            if os.path.exists(path):
                config_path = path
                break

    DDPREF.loadPreferences(config_path) # If still None, nothing will load, we are safe

def loadDatabase(dbname):
    pass

def loadHandlers():
    encounter_handler_spec = DDPREF.getPreference("handlers/encounters")

    for encounter_event_name in encounter_handler_spec.keys():
        for handler_name in encounter_handler_spec[encounter_event_name]:
            Handlers.registerEncounterEvent(handler_name)

def processAll(folders, walk_only=False, resolve_only=False):
    if not resolve_only:
        for top_dir in args.obj.folders:
            walk(top_dir, args_obj.walk_only)

    if not walk_only:
        resolve(args_obj.resolve)
    
def main(args):
    args_obj = parseArguments(args)
    loadPreferences(args_obj.config)
    loadDatabase(args_obj.database)
    loadHandlers()
    
    processAll(args_obj.folders, walk_only=args_obj.walk_only, resolve_only=args_obj.resolve)
