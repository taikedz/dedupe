import os.path
import time

import ddexceptions as dde

EVT_WALK_ENTERDIR = 'ENTER_DIR'
EVT_WALK_ENCOUNTERDIR = 'ENCOUNTER_DIR'
EVT_WALK_ENCOUNTERFILE = 'ENCOUNTER_FILE'

class DDHandlerRegistrar:
    def __init__(self):
        self.handlers = {}

    def registerHandler(self, event_name, *handlers):
        self.handlers[event_name] = handlers

class DDWalkerFactory(DDHandlerRegistrar):
    """ The factory is the starting point for registering event handlers.
    Once all events are registered, we start generating walkers for each folder,
    and do not let the factory receive new configurations
    """

    def produceWalker(self, targetpath):
        return DDWalker(targetpath, self.handlers)

class DDWalker:
    def __init__(self, targetpath, *handlers):
        self.toppath = targetpath
        self.handlers = handlers # map
        self.encounter_queue = [targetpath]

    def descend(self, encountered_item):
        if encountered_item.isfile:
            raise DDWalkException("Tried to descend into non-driectory '%s'" %(encountered_item.filepath))

        try:
            self.__processEvent(EVT_WALK_ENTERDIR, encountered_item) # this may throw a state control exception

            children = encountered_item.listChildren()
            self.encounter_queue[0:0] = children # this notation allows inserting list elements to head, not the list itself
        except dde.DDStateControlException:
            # We skip the directory altogether
            pass

    def popTopItem(self):
        return DDEncounteredItem(self.encountered_queue.pop(0) )

    def checkTopItem(self):
        return DDEncounteredItem(self.encountered_queue[0] )

    def walk(self):
        # Initial call is on directory, just descend
        self.descend(self.popTopItem() )

        while len(self.encounter_queue) > 0:
            self.__processItem(self.popTopItem() )

    def __processTopItem(self):
        target_item = self.popTopItem()
        event_name = None

        if target_item.isfile:
            event_name = EVT_WALK_ENCOUNTERFILE
        elif not target_item.isfile:
            event_name = EVT_WALK_ENCOUNTERDIR

        try:
            self.__processEvent(event_name, target_item)
        except dde.DDStateControlException:
            # Just interrupt processing for other handlers on event
            pass


    def __processEvent(self, event_name, target_item, raise_error=False):
        for handler in self.handlers[event_name]
                handler.process(target_item)

class DDEncounteredItem:
    def __init__(self, filepath):
        self.filepath = filepath
        self.islink = False

        if not os.path.exists(filepath):
            raise DDWalkException("No such file: %s" %(filepath))
        
        if os.path.isfile(filepath):
            self.isfile = True
        elif os.path.isdir(filepath):
            self.isfile = False

        if os.path.islink(filepath):
            self.islink = True

    def listChildren(self):
        children = os.listdir()
        children.sort()

        for i in range(len(children)):
            children[i] = "%s%s%s" % (self.filepath, os.path.sep, children[i])

        return children

if False:
    walk_handlers = { # this is how it will look once extracted from config?
        "ENTER_DIR" : ["RepoCheck"],
        "ENCOUNTER_FILE" : ["IgnoreCheck", "DeleteCheck", "Identify"],
        "ENCOUNTER_DIR" : ["SymLinkCheck", "IgnoreCheck", "DeleteCheck", "Descend"],
    }

    for event, handlers in walk_handlers:
        walker_factory = DDWalkerFactory()
        walker_factory.registerWalkHandler(event, *handlers)
