import pyximport; 
pyximport.install(setup_args = {"script_args" : ["--force"]},
                  language_level=3)

import unittest

from coutcatcher.coutcatcher import CoutCatcher
from cprinter import print_to_stdout


class CoutCatcherTester(unittest.TestCase): 

   def test_streams_flushed(self):
      print_to_stdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_stdout(b"bbbb");
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")

   def test_really_stops(self):
      print_to_stdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_stdout(b"bbbb")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")
      print_to_stdout(b"aaaa")
      res = catcher.stop_and_read()
      self.assertTrue(res is None)

   def test_restart(self):
      print_to_stdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_stdout(b"bbbb")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")
      print_to_stdout(b"aaaa")
      catcher.start()
      print_to_stdout(b"ccc")
      res = catcher.stop_and_read()
      self.assertTrue(res, "ccc")

   def test_second_start_ignored(self):
      print_to_stdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_stdout(b"bbbb")
      catcher.start()
      print_to_stdout(b"cccc")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbbcccc")
