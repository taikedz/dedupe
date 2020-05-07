import sys

## Codes - define here

DD_ERR_NOTIMPLEMENTED = 255

DD_ERR_OPTIONS = 10

DD_ERR_PREFSLOADED = 11

DD_ERR_WALKER = 50
DD_ERR_WALKERCONFIG = 51

## =======

class DDError(Exception):
    def __init__(self, message, exitcode=99):
        Exception.__init__(self, message)
        self.exitcode = exitcode

    def terminate(self):
        print("=== FATAL ERROR ===")
        print(str(self) )
        sys.exit(self.exitcode)

    def warn(self):
        print("--- warning ---",end='')
        print(str(self) )
        return self.exitcode

class NotImplemented(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_NOTIMPLEMENTED)

## --------

class ProcessorSkipException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

## --------

class PreferencesLocked(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_PREFSLOADED)

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
