import unittest

from dedupe.event import register_handler, execute_handlers

class TestEvents(unittest.TestCase):
    def test_events(self):
        _handlers_executed = []

        def _a_handler(d):
            _handlers_executed.append("A")
            return d == "a"

        def _b_handler(d):
            _handlers_executed.append("B")
            return "b" in d

        def _reset_handler_count():
            nonlocal _handlers_executed
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

        assert not execute_handlers("undefined", None)
