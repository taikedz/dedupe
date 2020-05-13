#!/usr/bin/env python

improt ddpreferences as DDPREF

def main(args):
    args_obj = parseArguments(args)
    loadPreferences(args_obj.conf)
    loadDatabase(DDPREF.getPreference("config/engine/database"))
    loadHandlers(DDPREF.getPreference("handlers"))
    
    for top_dir in args.obj.folders:
        walk(top_dir)

    resolve()
