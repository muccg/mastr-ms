from django.utils import unittest
import dingus
from StringIO import StringIO
import logging
logger = logging.getLogger(__name__)

from mastrms.testutils import XDisplayTest
from mastrms.mdatasync_client.client.MSDataSyncAPI import DataSyncServer
from mastrms.mdatasync_client.client.config import MSDSConfig
from mastrms.mdatasync_client.client.test.testclient import TestClient
from mastrms.mdatasync_client.client.version import VERSION

class BasicClientTests(unittest.TestCase, XDisplayTest):
    """
    These are simple tests just to exercise all the dialogs in the
    data sync client.
    """
    def setUp(self):
        config = MSDSConfig()
        self.client = TestClient(config)

    def tearDown(self):
        self.client.quit()

    @classmethod
    def setUpClass(cls):
        cls.setup_display()
    @classmethod
    def tearDownClass(cls):
        cls.teardown_display()

    def test1_mainwindow(self):
        """Show main window on screen, check if it's visible."""
        self.assertTrue(self.client.m.win.IsShownOnScreen(),
                        "Window is on screen")

    def test2_tray_minimize_maximize(self):
        """Minimize window to tray, then unminimize it."""
        self.client.close() # doesn't seem to disappear window
        #self.assertFalse(self.client.m.win.IsShownOnScreen(),
        #                 "Window exists but is hidden")
        self.client.minimize()
        self.assertFalse(self.client.m.win.IsShownOnScreen(),
                         "Window exists but is hidden")
        self.client.activate_tray_icon()
        self.assertTrue(self.client.m.win.IsShownOnScreen(),
                        "Window is on screen again")

    @unittest.skip("this seems to be broken")
    def test3_preferences_window(self):
        """Exercise the code which shows preferences dialog."""
        prefs = self.client.click_menu_preferences()
        prefs.close()

    @unittest.skip("this is also broken with thread problems")
    def test4_advanced_preferences_window(self):
        """Exercise advanced preferences dialog code."""
        prefs = self.client.click_menu_preferences()
        advanced = prefs.click_advanced()
        advanced.advanced_click_close()
        prefs.close()

class _BetterPatcher(dingus._Patcher):
    def __enter__(self):
        self.patch_object()
        return self.new_object
def betterpatch(object_path, new_object=dingus.NoArgument):
    module_name, attribute_name = object_path.rsplit('.', 1)
    return _BetterPatcher(module_name, attribute_name, new_object)

class DataSyncServerTests(unittest.TestCase):
    """
    These are unit tests for the `DataSyncServer` class.
    """
    def setUp(self):
        self.config = MSDSConfig()
        self.server = DataSyncServer(self.config)

    @staticmethod
    def fake_urlopen(json, my_dingus=None):
        my_dingus = my_dingus or dingus.Dingus()
        urlopen = dingus.Dingus(return_value=StringIO(json))
        return betterpatch("urllib2.urlopen", urlopen)

    def test_handshake(self):
        """Try the "handshake" API call."""
        with self.fake_urlopen('{ "success": true, "details": { "host": "testhost", "flags": "testflags", "username": "username", "rootdir": "rootdir", "rules": ["a", "b", "c"] } }'):
            details = self.server.handshake()

            self.assertEqual(details["host"], "testhost")
            self.assertListEqual(details["rules"], ["a", "b", "c"])

    def test_handshake_weird_json(self):
        """Test handshaking when server returns unexpected json."""
        with self.assertRaises(KeyError):
            with self.fake_urlopen("{ lah: 'hello' }"):
                details = self.server.handshake()

    def test_handshake_not_json(self):
        """
        Test handshaking when server returns something other than json.
        This test case expects `KeyError`, which isn't ideal.
        """
        with self.assertRaises(KeyError):
            with self.fake_urlopen("  *8>--O===3  this is not json; it's an emu  "):
                details = self.server.handshake()

    def test_requestsync(self):
        """
        Tests calling the /sync/requestsync/ view. The fake server
        requests no files.
        """
        with self.fake_urlopen('{ "success": true, "details": { "host": "testhost", "flags": "testflags", "username": "username", "rootdir": "rootdir", "rules": ["a", "b", "c"] } }') as d:
            result = self.server.requestsync()
            self.assertTrue(result["success"])
            self.assertEqual(len(d.calls), 1)
            self.assertEqual(len(d.calls("()")), 1)
            self.assertTrue(d.calls("()", dingus.DontCare,
                                    "sync_completed=False&version=%s" % VERSION,
                                    dingus.DontCare).once())

    def test_requestsync_expected_files(self):
        """
        Tests calling /sync/requestsync, with 1 file requested by the
        fake server.
        """
        # fixme: this is the wrong place to test such things
        with self.fake_urlopen('{ "success": true, "details": {}, "files": { "1": { "test.txt": [1, 2, "relpath", false] } } }') as d:
            result = self.server.requestsync()
            logger.info(repr(d.calls))
            self.assertTrue(result["success"])

    def test_requestsync_baseurl(self):
        "tests requestsync when configured sync url has no trailing slash"
        self.config["synchub"] = "http://test"
        self.config["sitename"] = "b"
        self.config["stationname"] = "c"
        self.config["organisation"] = "a"
        my_dingus = dingus.Dingus()
        with self.fake_urlopen('{ "success": true, "details": {} }') as d:
            with dingus.patch("urllib2.Request", my_dingus):
                result = self.server.requestsync()
                self.assertTrue(result["success"])
                self.assertTrue(d.calls("()").once())
            self.assertEqual(len(my_dingus.calls), 1)
            self.assertEqual(my_dingus.calls[0].args[0], "http://test/requestsync/a/b/c/")

    def test_requestsync_urlopen_error(self):
        "test requestsync when urlopen raises an exception"
        with dingus.patch("urllib2.urlopen", dingus.exception_raiser(IOError("you fail"))):
            result = self.server.requestsync()
            self.assertFalse(result["success"])
            self.assertEqual(result["message"], "you fail")

    # todo: make tests for
    #  * DataSyncServer.checksamplefiles()
    #  * DataSyncServer.get_node_names()
    #  * DataSyncServer.send_key()  - this uses yaphc
    #  * DataSyncServer.send_log()  - this uses yaphc
