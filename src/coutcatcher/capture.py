from contextlib import contextmanager

from .coutcatcher import CoutCatcher

class CatcherContext:
    def __init__(self, as_stream=False):
        self.as_stream = as_stream
        self._cout = CoutCatcher("stdout")
        self._cerr = CoutCatcher("stderr")
        self.cout = None
        self.cerr = None

    def __enter__(self):
        self._cout.start()
        self._cerr.start()
        return self

    def __exit__(self, *exc):
        if self.as_stream:
            self.cout=self._cout.stop()
            self.cerr=self._cerr.stop()
        else:
            self.cout=self._cout.stop_and_read()
            self.cerr=self._cerr.stop_and_read()

    def close(self):
        if self.as_stream:
            if self.cout is not None:
                self.cout.close()
            if self.cerr is not None:
                self.cerr.close()

    

def capture(as_stream=False):
    return CatcherContext(as_stream)
