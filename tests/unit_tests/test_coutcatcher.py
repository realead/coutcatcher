import sys
import unittest

from coutcatcher.coutcatcher import CoutCatcher, print_to_cstdout, print_to_cstderr


class CoutCatcherTester(unittest.TestCase): 

   def test_streams_flushed(self):
      print_to_cstdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_cstdout(b"bbbb");
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")

   def test_really_stops(self):
      print_to_cstdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_cstdout(b"bbbb")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")
      print_to_cstdout(b"aaaa")
      res = catcher.stop_and_read()
      self.assertTrue(res is None)

   def test_restart(self):
      print_to_cstdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_cstdout(b"bbbb")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")
      print_to_cstdout(b"aab\nbaa")
      catcher.start()
      print_to_cstdout(b"ccc")
      res = catcher.stop_and_read()
      self.assertTrue(res, "ccc")

   def test_second_start_ignored(self):
      print_to_cstdout(b"a")
      catcher = CoutCatcher()
      catcher.start()
      print_to_cstdout(b"bbbb")
      catcher.start()
      print_to_cstdout(b"cccc")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbbcccc")

   def test_sys_stdout_catched_too(self):
      catcher = CoutCatcher()
      catcher.start()
      sys.__stdout__.write("a")
      catcher.start()
      res = catcher.stop_and_read()
      self.assertEqual(res, "a")



class CerrCatcherTester(unittest.TestCase): 

   def test_streams_flushed(self):
      print_to_cstdout(b"a")
      catcher = CoutCatcher("stderr")
      catcher.start()
      print_to_cstderr(b"bbbb");
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")

   def test_really_stops(self):
      print_to_cstdout(b'First\n')
      print_to_cstdout(b"a")
      catcher = CoutCatcher("stderr")
      catcher.start()
      print_to_cstderr(b"bbbb")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")
      print_to_cstderr(b"aaaa")
      res = catcher.stop_and_read()
      self.assertTrue(res is None)

   def test_restart(self):
      print_to_cstdout(b"a")
      catcher = CoutCatcher("stderr")
      catcher.start()
      print_to_cstderr(b"bbbb")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbb")
      print_to_cstderr(b"\naaaaBB")
      catcher.start()
      print_to_cstderr(b"ccc")
      res = catcher.stop_and_read()
      self.assertTrue(res, "ccc")

   def test_second_start_ignored(self):
      print_to_cstdout(b"a")
      catcher = CoutCatcher("stderr")
      catcher.start()
      print_to_cstderr(b"bbbb")
      catcher.start()
      print_to_cstderr(b"cccc")
      res = catcher.stop_and_read()
      self.assertEqual(res, "bbbbcccc")

   def test_sys_stderr_catched_too(self):
      catcher = CoutCatcher("stderr")
      catcher.start()
      sys.__stderr__.write("a")
      catcher.start()
      res = catcher.stop_and_read()
      self.assertEqual(res, "a")
