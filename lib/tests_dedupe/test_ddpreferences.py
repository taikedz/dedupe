import unittest

import ddpreferences as DDPREF
import ddexceptions as DDE
import ddlog

import testutils as TU

#ddlog.setLevel("DEBUG")

class PreferencesCheck(unittest.TestCase):
    
    def setUp(self):
        DDPREF.loadPreferences(TU.touch("testfile.yaml", data="""
level1:
    level2:
        key1: "value1"
        """) )

    def runTest(self):
        self.assertEqual(DDPREF.getPreference("level1/level2")["key1"], "value1" )
        self.assertTrue(not "key2" in DDPREF.getPreference("level1/level2").keys())

        DDPREF.setDefaultPreferences("level1/level2", {"key2":"value2", "key1": "default_value"})
        self.assertTrue("key2" in DDPREF.getPreference("level1/level2").keys())
        self.assertEqual(DDPREF.getPreference("level1/level2")["key2"], "value2" )
        self.assertEqual(DDPREF.getPreference("level1/level2")["key1"], "value1" )

        DDPREF.setDefaultPreferences("prefs/not/from/file", {"pref":"data"})
        self.assertEqual(DDPREF.getPreference("prefs/not/from/file")["pref"], "data" )

        TU.assertRaises(self, DDE.PreferenceUnknown, DDPREF.getPreference, "prefs/unknown")

    def tearDown(self):
        TU.removeTmp()

if __name__ == "__main__":
    unittest.main()
