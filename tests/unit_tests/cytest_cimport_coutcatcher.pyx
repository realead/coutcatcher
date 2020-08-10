import unittest

cimport coutcatcher.coutcatcher as ccoutcatcher

class Cimpor_coutcatcher_Tester(unittest.TestCase): 

    def test_cimport_getit(self):
        self.assertEqual(ccoutcatcher.getit(), 21)
