import unittest

import re
import argparse

import ddexceptions as dde
import ddargparse as ddap

class DDArgTests(unittest.TestCase):
    def test_resolvewalk(self):
        print("Resolve/walk tests")

        # These should be fine
        self.assertIsInstance(ddap.parseArguments(["--resolve"]), argparse.Namespace)
        self.assertIsInstance(ddap.parseArguments(["--walk-only"]), argparse.Namespace)

        # This should error - only one may be specified
        self.assertRaises(dde.DDOptionsError, ddap.parseArguments, ["--resolve", "--walk-only"])

        # This should error - in "resolve" mode, no folders should be permitted
        self.assertRaises(dde.DDOptionsError, ddap.parseArguments, ["--resolve", "a"])

if __name__ == "__main__":
    unittest.main()
