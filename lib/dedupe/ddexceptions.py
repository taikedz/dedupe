import sys

## Codes - define here

DD_ERR_OPTIONS = 10

## =======

class DDError(Exception):
    def __init__(self, message, exitcode=99):
        Exception.__init__(self, message)
        self.exitcode = exitcode

    def terminate(self):
        print("=== FATAL ERROR ===")
        print(str(self) )
        exit(self.exitcode)

    def warn(self):
        print("--- warning ---",end='')
        print(str(self) )


class DDOptionsError(DDError):
    def __init__(self, message):
        DDError.__init__(self, message, DD_ERR_OPTIONS)
