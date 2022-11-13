from typing import Any
from dedupe.errors import DedupeError


__EVENTS = {}

class HandlerImplementationError(DedupeError): pass


def register_handler(event_name, handler):
    if not callable(handler):
        raise HandlerImplementationError(f"{type(handler)}:{handler} is not callable.")

    if __EVENTS.get(event_name) is None:
        __EVENTS[event_name] = []

    __EVENTS[event_name].append(handler)


def execute_handlers(event_name:str, data:Any) -> bool:
    """ Execute handlers registered for a given event.

    If a handler returns a value resolving as True, further handlers are not called, and execute_handlers returns True.

    If no handlers return True, execute_handlers returns False
    """
    for handler in __EVENTS.get(event_name, []):
        was_handled = bool(handler(data))
        if was_handled is True:
            return True
    return False

