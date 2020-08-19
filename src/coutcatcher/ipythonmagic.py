import sys
from .capture import capture

_capture = None

def  start_capture():
    global _capture
    _capture = capture()
    _capture.__enter__()

def stop_capture():
    global _capture
    if _capture is not None:
        _capture.__exit__(None, None, None)
        sys.stdout.write(_capture.cout)
        sys.stderr.write(_capture.cerr)
        _capture = None
     

def load_ipython_extension(ip):
    """Registers coutcatcher as an IPython extension
    
    Captures all C output during execution and forwards to sys.
    
    Use: %load_ext coutcatcher
    """
    ip.events.register('pre_execute', start_capture)
    ip.events.register('post_execute', stop_capture)


def unload_ipython_extension(ip):
    """Unload coutcatcher as an IPython extension
    
    Use: %load_ext coutcatcher
    """
    stop_capture() # make sure capturing is stopped
    ip.events.unregister('pre_execute', start_capture)
    ip.events.unregister('post_execute', stop_capture)
