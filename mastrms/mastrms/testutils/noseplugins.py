from nose.plugins import Plugin
import logging

__all__ = ["SilenceSouthPlugin"]


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
        logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(
            self.south_logging_level)
