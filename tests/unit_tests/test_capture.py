import sys
import unittest

from coutcatcher import capture
from coutcatcher.coutcatcher import print_to_cstdout, print_to_cstderr


class CaptureTester(unittest.TestCase): 

    def test_as_string(self):
        with capture() as c:
            print_to_cstdout(b"a\n")
            print_to_cstderr(b"b\n")
        self.assertEqual(c.cout, "a\n")
        self.assertEqual(c.cerr, "b\n")

    def test_as_stream(self):
        with capture(True) as c:
            print_to_cstdout(b"a\n")
            print_to_cstderr(b"b\n")
        self.assertEqual(c.cout.read(), "a\n")
        self.assertEqual(c.cerr.read(), "b\n")
        c.close()


