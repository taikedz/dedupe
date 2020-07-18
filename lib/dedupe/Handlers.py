import ddlog
import ddexceptions as DDE
log = ddlog.getLogger("dedupe")


EVT_ENTER_DIR = "EVT_ENTER_DIR"
EVT_ENCOUNTER_DIR = "EVT_ENCOUNTER_DIR"
EVT_ENCOUNTER_FILE = "EVT_ENCOUNTER_FILE"
EVT_IDENTIFY = "EVT_IDENTIFY"

__all_handlers = {
    EVT_ENTER_DIR: [],
    EVT_ENCOUNTER_DIR: [],
    EVT_ENCOUNTER_FILE: [],
    EVT_IDENTIFY: [],
}

class WalkEventHandler:
    """
    A callable object representing an event handler.

    If you are creating a handler, please use registerWalkEventHandler()
     Do not use this class directly.
    """
    def __init__(self, handler_name, function_definition):
        self.handler_name = handler_name
        self.function_definition = function_definition
        log.debug("Registered WalkEventHandler for %s" %(handler_name) )

    def __str__(self):
        return self.handler_name

    def __call__(self, target_item):
        log.debug("Called %s on <%s>" % (self.handler_name, target_item))
        self.function_definition(target_item)

def registerWalkEventHandler(event_name, handler_name, function_definition=None):
    """
    Register a walk event handler either by providing a function, or a handler name alone.
    If several handlers are registered with the same name, all will be called (handlers are not over-written).

    If function_definition supplies a callable, this is associated to the handler name.

    If function_definition is not supplied, attempts to load that handler from the first `handlers` directory found in PYTHONPATH

    For example, calling
    
        registerWalkEventHandler(Handlers.EVT_ENCOUNTER_FILE, "DeleteCheck")

    will attempt to import a module handlers.DeleteCheck
    """
    log.debug("Registering %s on %s" %(handler_name, event_name))
    if function_definition == None:
        if handler_name.find(".") < 0 :
            handler_name = "handlers."+handler_name

        handler = importlib.import_module(handler_name)
        function_definition = handler.process
    elif not callable(function_definition):
        raise DDE.FunctionDefinitionError("A non-function was provided for handler registration '%s' on '%s'"%(handler_name, event_name) )

    __all_handlers[event_name].append( WalkEventHandler(handler_name, function_definition) )

def processEvent(event_name, current_item):
    """ Runs the handlers associated with the named event. If the handler returns a message, logs the message.
    """
    log.debug("Event [%s] :: %s" % (event_name, current_item.getName()) )
    for handler in __all_handlers[event_name]:
        result = handler(current_item)
        if result != None:
            log.info(str(result) )
