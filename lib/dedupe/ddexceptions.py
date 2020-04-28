import sys

## Codes - define here

DD_ERR_OPTIONS = 10

DD_ERR_WALKERCONFIG = 50

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

class DDStateControlException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

## --------

class DDOptionsError(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_OPTIONS)

class DDWalkerConfigException(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, exitcode=DD_ERR_WALKERCONFIG)
