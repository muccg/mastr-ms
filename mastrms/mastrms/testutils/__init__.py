import logging
import os

__all__ = ["MockLoggingHandler", "XDisplayTest"]

class MockLoggingHandler(logging.Handler):
    """
    Mock logging handler to check for expected logs.
    http://stackoverflow.com/a/1049375
    """
    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }

class XDisplayTest(object):
    """
    This TestCase mixin provides a virtual X server if DISPLAY is not
    set.
    """
    @classmethod
    def setup_display(cls):
        if not os.environ.get("DISPLAY"):
            logging.info("Using Xvfb for display")
            from xvfbwrapper import Xvfb
            cls.vdisplay = Xvfb()
            cls.vdisplay.start()
        else:
            cls.vdisplay = None

    @classmethod
    def teardown_display(cls):
        if cls.vdisplay:
            cls.vdisplay.stop()
