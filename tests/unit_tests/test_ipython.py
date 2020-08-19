import unittest

from coutcatcher import capture
from coutcatcher.coutcatcher import print_to_cstdout, print_to_cstderr

try:
    import IPython.testing.globalipapp
    import  IPython.testing.tools as tt
except ImportError:
    # Disable tests and fake helpers for initialisation below.
    def skip_if_not_installed(_):
        return None
else:
    def skip_if_not_installed(c):
        return c

try:
    # disable IPython history thread before it gets started to avoid having to clean it up
    from IPython.core.history import HistoryManager
    HistoryManager.enabled = False
except ImportError:
    pass


@skip_if_not_installed
class IPythonTester(unittest.TestCase): 

    def test_whole_workflow(self):
        self.assertTrue(True)
        # ToDo: how to test?
        #with tt.AssertPrints("first"):
        #     ip = IPython.testing.globalipapp.get_ipython()
        #    ip.ex('from coutcatcher.coutcatcher import print_to_cstdout, print_to_cstderr')
        #    ip.run_line_magic('load_ext', 'coutcatcher')
        #    ip.ex('print_to_cstdout(b"first")')
        #    ip.run_line_magic('unload_ext', 'coutcatcher') 
        #    ip.ex('print_to_cstdout(b"second")')

