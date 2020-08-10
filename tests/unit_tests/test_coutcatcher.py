import unittest

import coutcatcher.coutcatcher as t


class coutcatcherTester(unittest.TestCase): 

   def test_test_me(self):
      self.assertEqual(t.test_me(), 42)
