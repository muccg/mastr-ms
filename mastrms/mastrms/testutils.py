from nose.plugins import Plugin
import logging
import os

__all__ = ["SilenceSouthPlugin", "MockLoggingHandler", "XDisplayTest"]

class SilenceSouthPlugin(Plugin):
    """
    South logs a lot while it does migrations in the test setup
    stage. This nose plugin shuts it up, courtesy:
    http://pypede.wordpress.com/2012/06/17/disable-south-debug-logging-when-testing-apps-with-nose-in-django/
    """
    south_logging_level = logging.ERROR

    def configure(self, options, conf):
        super(SilenceSouthPlugin, self).configure(options, conf)
        logging.getLogger('south').setLevel(self.south_logging_level)
        logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(self.south_logging_level)

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
