import sys

import ddlog

log = ddlog.getLogger("dedupe")

## Codes - define here

DD_ERR_NOTIMPLEMENTED = 255

DD_ERR_OPTIONS = 10

DD_ERR_PREFSLOADED = 11
DD_ERR_PREFUNKNOWN = 12

DD_ERR_WALKER = 50
DD_ERR_WALKERCONFIG = 51

DD_ERR_FUNCDEF = 60

## =======

class DDError(Exception):
    """
    General error

    Any DDError can cause the program to terminate by invoking its terminate() call

    Alternatively, a DDError can be used to log a warning instead.

    Errors should carry their own exit code, in case an exit is required.
    """
    def __init__(self, message, exitcode=99):
        Exception.__init__(self, message)
        self.exitcode = exitcode

    def terminate(self):
        log.error("=== FATAL ERROR ===")
        log.error(str(self) )
        sys.exit(self.exitcode)

    def warn(self):
        log.warn("--- warning ---",end='')
        log.warn(str(self) )
        return self.exitcode

class NotImplemented(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_NOTIMPLEMENTED)

## --------

class ProcessorSkipException(Exception):
    """
    A special exception which indicates that processing for an item should be stopped and abandoned.
    """
    def __init__(self, message):
        Exception.__init__(self, message)

## --------

class PreferencesLocked(DDError):
    """
    Preferences must be loaded before overlaying defaults.

    Trying to specify defaults before loading prefs restuls in this exception.
    """
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_PREFSLOADED)

class PreferenceUnknown(DDError):
    """
    The specified preference is undefined and cannot be assumed.
    """
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_PREFUNKNOWN)

## --------

class OptionsError(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_OPTIONS)

class WalkerConfigException(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_WALKERCONFIG)

class WalkerException(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_WALKER)

## --------

class FunctionDefinitionError(DDError):
    """
    An attempt to register a handler provided a non-callable item instead of a function/callable.
    """
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_FUNCDEF)
