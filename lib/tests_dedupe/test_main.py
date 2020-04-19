import unittest

# We need to import the classes to the current context, or `unittest` will not pick them up
from test_args import *

if __name__ == "__main__":
    print("Running all tests ...")
    unittest.main()
