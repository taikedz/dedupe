import ddlog
log = ddlog.getLogger("dedupe")


EVT_ENTER_DIR = "EVT_ENTER_DIR"
EVT_ENCOUNTER_DIR = "EVT_ENCOUNTER_DIR"
EVT_ENCOUNTER_FILE = "EVT_ENCOUNTER_FILE"

all_handlers = {
    EVT_ENTER_DIR: [],
    EVT_ENCOUNTER_DIR: [],
    EVT_ENCOUNTER_FILE: [],
}

class WalkEventHandler:
    def __init__(self, handler_name, function_definition):
        self.handler_name = handler_name
        self.function_definition = function_definition
        log.debug("Registered WalkEventHandler for %s" %(handler_name) )

    def __str__(self):
        return self.handler_name

    def process(self, target_item):
        log.debug("Called %s on <%s>" % (self.handler_name, target_item))
        self.function_definition(target_item)

def registerWalkEventHandler(event_name, handler_name, function_definition):
    log.debug("Registering %s on %s" %(handler_name, event_name))
    all_handlers[event_name].append( WalkEventHandler(handler_name, function_definition) )

def getHandlers():
    return all_handlers
