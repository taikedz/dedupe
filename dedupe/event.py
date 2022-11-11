from typing import Any
from dedupe.errors import DedupeError


__EVENTS = {}

class HandlerImlementationError(DedupeError): pass


def register_handler(event_name, handler):
    if not callable(handler):
        raise HandlerImlementationError(f"{type(handler)}:{handler} is not callable.")

    if __EVENTS.get(event_name) is None:
        __EVENTS[event_name] = []

    __EVENTS[event_name].append(handler)


def execute_handlers(event_name:str, data:Any) -> bool:
    """ Execute handlers registered for a given event.

    If a handler returns True, further handlers are not called, and execute_handlers returns True.

    If no handlers return True, execute_handlers returns False
    """
    for handler in __EVENTS[event_name]:
        res = handler(data)
        if res is True:
            return True
    return False



if __name__ == "__main__":
    _handlers_executed = []

    def _a_handler(d):
        _handlers_executed.append("A")
        return d == "a"

    def _b_handler(d):
        _handlers_executed.append("B")
        return "b" in d

    def _reset_handler_count():
        global _handlers_executed
        _handlers_executed = []

    register_handler("test", _a_handler)
    register_handler("test", _b_handler)

    assert execute_handlers("test", "a")
    assert _handlers_executed == ["A"]
    _reset_handler_count()

    assert execute_handlers("test", "abacus")
    assert _handlers_executed == ["A", "B"]
    _reset_handler_count()

    assert not execute_handlers("test", "other")
    assert _handlers_executed == ["A", "B"]
    _reset_handler_count()

    print("Basic tests passed")
