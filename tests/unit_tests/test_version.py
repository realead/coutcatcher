import unittest

import coutcatcher


class VersionTester(unittest.TestCase): 

   def test_major(self):
      self.assertEqual(coutcatcher.__version__[0], 0)

   def test_minor(self):
      self.assertEqual(coutcatcher.__version__[1], 1)

   def test_last(self):
      self.assertEqual(coutcatcher.__version__[2], 0)
