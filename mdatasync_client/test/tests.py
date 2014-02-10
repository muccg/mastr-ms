from django.utils import unittest
import dingus
import os.path
import tempfile
from StringIO import StringIO
import logging
logger = logging.getLogger(__name__)

from mastrms.testutils import XDisplayTest
from mastrms.mdatasync_client.client.MSDataSyncAPI import DataSyncServer, MSDataSyncAPI, MSDSImpl
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
        self.client = TestClient(config, timeout=120)

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
            with self.fake_urlopen("{ 'lah': 'hello' }"):
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

    def test_requestsync_spaces(self):
        self.config["synchub"] = "http://test"
        self.config["sitename"] = "An Interesting Site"
        self.config["stationname"] = "A Station Name"
        self.config["organisation"] = "The Organisation"

        my_dingus = dingus.Dingus()
        with self.fake_urlopen('{ "success": true, "details": {} }') as d:
            with dingus.patch("urllib2.Request", my_dingus):
                result = self.server.requestsync()
                self.assertTrue(result["success"])
                self.assertTrue(d.calls("()").once())
            self.assertEqual(len(my_dingus.calls), 1)
            self.assertEqual(my_dingus.calls[0].args[0], "http://test/requestsync/The%20Organisation/An%20Interesting%20Site/A%20Station%20Name/")

    # todo: make tests for
    #  * DataSyncServer.checksamplefiles()
    #  * DataSyncServer.get_node_names()
    #  * DataSyncServer.send_key()  - this uses yaphc
    #  * DataSyncServer.send_log()  - this uses yaphc

def msds_log(msg, *args, **kwargs):
    logger.info("MSDS: %s" % msg)
msds_log.LOG_ERROR = 0

class MSDataSyncAPITests(unittest.TestCase):
    """
    This class is for unit tests of the `MSDataSyncAPI` class.
    At present, there is only one test.
    """
    def setUp(self):
        self.config = MSDSConfig()
        self.api = MSDataSyncAPI(self.config, msds_log)

    def test1_find_local_file_or_directory(self):
        """
        Tests `MSDataSyncAPI.find_local_file_or_directory()`. Checks
        that TEMP files are correctly removed from list of files to
        copy to staging directory.
        """
        wanted_filename = "asdf"
        path = "/path/to/this/dir"
        p = lambda f: os.path.join(path, f)

        # localfiledict - as specified in MSDataSyncAPI.getFiles() docstring
        lfd = {
            ".": ["1", "2", "3"],
            "/": path,
            "asdf": {
                ".": ["a", "b", "c", "TEMPBASE", "TEMPDAT", "TEMPDIR",
                      "TEMP", "TEMPprefix", "suffixTEMP"],
                "/": p("asdf"),
                },
            "qwerty": {
                ".": ["A", "B", "C", "TEMPBASE", "TEMPDAT", "TEMPDIR"],
                "/": p("qwerty"),
                "hjkl": {
                    ".": ["h", "j", "k", "l"],
                    "/": p("qwerty/hjkl"),
                    },
                "zxc": {
                    ".": ["z", "x", "c", "tempqwerty"],
                    "/": p("qwerty/zxc"),
                    },
                },
            "foo": {
                ".": ["X", "Y", "Z"],
                "/": p("foo"),
                },
            "bar": {
                ".": ["4", "5", "6"],
                "/": p("bar"),
                },
            "suffix": {
                ".": ["S1", "S2", "S3", "suffixTEMP"],
                "/": p("suffix"),
                },
            "baz": {
                ".": ["B1", "B2", "B3", "temp"],
                "/": p("baz"),
                },
            }

        result = self.api.find_local_file_or_directory(lfd, "asdf")
        self.assertIsNone(result, "asdf skipped")

        result = self.api.find_local_file_or_directory(lfd, "qwerty")
        self.assertIsNone(result, "qwerty skipped")

        result = self.api.find_local_file_or_directory(lfd, "foo")
        self.assertTrue(bool(result), "subdirectory")

        result = self.api.find_local_file_or_directory(lfd, "bar")
        self.assertEqual(result, p("bar"), "another subdirectory")

        result = self.api.find_local_file_or_directory(lfd, "2")
        self.assertEqual(result, p("2"), "file at top level")

        # this one is surprising maybe
        result = self.api.find_local_file_or_directory(lfd, "B")
        self.assertEqual(result, p("qwerty/B"), "file within ignored directory")

        result = self.api.find_local_file_or_directory(lfd, "Y")
        self.assertEqual(result, p("foo/Y"), "file within subdirectory")

        result = self.api.find_local_file_or_directory(lfd, "suffix")
        self.assertEqual(result, p("suffix"), "TEMP at end of filename")

        result = self.api.find_local_file_or_directory(lfd, "baz")
        self.assertIsNone(result, "lowercase TEMP")

        # this one is also surprising maybe?
        result = self.api.find_local_file_or_directory(lfd, "hjkl")
        self.assertEqual(result, p("qwerty/hjkl"), "subdir within excluded dir")

        result = self.api.find_local_file_or_directory(lfd, "zxc")
        self.assertIsNone(result, "excluded subdir within excluded dir")

class MSDSImplTests(unittest.TestCase):
    """
    These are unit tests for the `MSDSImpl` class.
    """
    def setUp(self):
        self.config = MSDSConfig(localdir=tempfile.mkdtemp())
        self.api = MSDataSyncAPI(self.config, msds_log)
        self.impl = MSDSImpl(msds_log, self.api)

        # method stub
        self.api.post_sync_step = dingus.Dingus()

        def remove_localdir():
            os.rmdir(self.config["localdir"])
        self.addCleanup(remove_localdir)

        self.rsyncconfig = self.RemoteSyncParamsStub({
                "filename1": (False, False), # this file didn't change
                "filename2": (False, False), # this file didn't change
                "filename3": (False, True),  # this file changed
                "asdf": (False, True),       # this file changed
                })

        self.filename_id_map = {
            "filename1": (1, 10),
            "filename2": (2, 20),
            "filename3": (3, 30),
            "filename4": (4, 40),
        }

    # serverCheckRunSampleFiles method only uses the
    # file_changes member of RemoteSyncParams, so stub it
    class RemoteSyncParamsStub(object):
        def __init__(self, file_changes):
            self.file_changes = file_changes

    def test1_check_run_sample_files(self):
        """
        Check that `MSDSImpl.serverCheckRunSampleFiles()` results in
        an API call marking complete the correct samples.
        """
        Server = dingus.Dingus()
        with dingus.patch("mastrms.mdatasync_client.client.MSDataSyncAPI.DataSyncServer", Server):
            self.impl.serverCheckRunSampleFiles(self.rsyncconfig,
                                                self.filename_id_map)

        self.assertEqual(len(Server.return_value.calls), 1,
                         "One DataSyncServer instance is created")

        runsampledict, last_error = Server.return_value.calls[0][1]

        self.assertEqual(len(runsampledict), 2,
                         "Two samples are marked complete")
        self.assertEqual(runsampledict, { 1: [10], 2: [20] },
                         "The correct samples are marked complete")

    def create_data_file(self, *path):
        temp_name = os.path.join(self.config["localdir"], *path)
        os.makedirs(os.path.dirname(temp_name))
        open(temp_name, "w").close()

        def cleanup(temp_name, nparents):
            logger.debug("removing %s" % temp_name)
            os.remove(temp_name)
            for p in range(nparents):
                temp_name = os.path.dirname(temp_name)
                logger.debug("rmdir %s" % temp_name)
                os.rmdir(temp_name)

        self.addCleanup(cleanup, temp_name, len(path) - 1)

    def test2_check_run_sample_files_temp_files(self):
        """
        Sample is not marked incomplete if there is a TEMP file in its
        directory.
        """
        # create a file called TEMP within a directory called
        # filename2 somewhere within the data dir
        self.create_data_file("test", "dir", "filename2", "TEMP")

        Server = dingus.Dingus()
        with dingus.patch("mastrms.mdatasync_client.client.MSDataSyncAPI.DataSyncServer", Server):
            self.impl.serverCheckRunSampleFiles(self.rsyncconfig,
                                                self.filename_id_map)

        self.assertEqual(len(Server.return_value.calls), 1,
                         "One DataSyncServer instance is created")

        runsampledict, last_error = Server.return_value.calls[0][1]

        self.assertEqual(len(runsampledict), 1,
                         "One sample is marked complete")
        self.assertEqual(runsampledict, { 1: [10] },
                         "The correct sample is marked complete")

    def test_parse_rsync_changes_empty_dir(self):
        """
        Check parsing of rsync output -- changed and unchanged files
        and directories.
        """
        data = """
.d          ./
.d          runs/
.d          runs/2013/
.d          runs/2013/7/
.d          runs/2013/7/475/
cd+++++++++ runs/2013/7/475/solvent_475-50479.d/
.d          runs/2013/7/475/sweep_475-50563.d/
<f..T...... runs/2013/7/475/sweep_475-50563.d/DATA.MS
<f..T...... runs/2013/7/475/sweep_475-50563.d/GC.ini
<f..T...... runs/2013/7/475/sweep_475-50563.d/PRE_POST.INI
<f..T...... runs/2013/7/475/sweep_475-50563.d/acqmeth.txt
<f..T...... runs/2013/7/475/sweep_475-50563.d/cnorm.ini
<f..T...... runs/2013/7/475/sweep_475-50563.d/runstart.txt
<f..T...... runs/2013/7/475/sweep_475-50563.d/tic_front.csv
"""

        changes = MSDSImpl.parse_rsync_changes(data)

        self.assertEqual(changes["runs/2013/7/475/solvent_475-50479.d"],
                         (True, True))
        self.assertEqual(changes["runs/2013/7/475/sweep_475-50563.d"],
                         (True, False))
        self.assertEqual(changes["runs/2013/7/475"],
                         (True, True))
        self.assertEqual(changes["runs"],
                         (True, True))
        # self.assertEqual(changes["."],
        #                  (True, True))

    def test_parse_rsync_changes_propagate(self):
        """
        Check propagation of file changes to parent directories.
        """
        data = """
.d          ./
.d          runs/
.d          runs/2013/
.d          runs/2013/7/
.d          runs/2013/7/475/
cd+++++++++ runs/2013/7/475/solvent_475-50479.d/
.d          runs/2013/7/475/sweep_475-50563.d/
<f..T...... runs/2013/7/475/sweep_475-50563.d/DATA.MS
<f..T...... runs/2013/7/475/sweep_475-50563.d/GC.ini
<f..T...... runs/2013/7/475/sweep_475-50563.d/PRE_POST.INI
<f+.T...... runs/2013/7/475/sweep_475-50563.d/acqmeth.txt
<f..T...... runs/2013/7/475/sweep_475-50563.d/cnorm.ini
<f..T...... runs/2013/7/475/sweep_475-50563.d/runstart.txt
<f..T...... runs/2013/7/475/sweep_475-50563.d/tic_front.csv
"""
        changes = MSDSImpl.parse_rsync_changes(data)

        self.assertEqual(changes["runs/2013/7/475/solvent_475-50479.d"],
                         (True, True),
                         "runs/2013/7/475/solvent_475-50479.d")
        self.assertEqual(changes["runs/2013/7/475/sweep_475-50563.d"],
                         (True, True),
                         "runs/2013/7/475/sweep_475-50563.d")
        self.assertEqual(changes["runs/2013/7/475/sweep_475-50563.d/DATA.MS"],
                         (False, False),
                         "runs/2013/7/475/sweep_475-50563.d/DATA.MS")
        self.assertEqual(changes["runs/2013/7/475/sweep_475-50563.d/acqmeth.txt"],
                         (False, True),
                         "runs/2013/7/475/solvent_475-50479.d/acqmeth.txt")


    def test_parse_rsync_changes_cull(self):
        """
        Check culling of empty directories from file_changes map.
        """
        changes = {
            '.': (True, True),
            'runs': (True, True),
            'runs/2013': (True, True),
            'runs/2013/7': (True, True),
            'runs/2013/7/475': (True, True),
            'runs/2013/7/475/solvent_475-50479.d': (True, True),
            'runs/2013/7/475/sweep_475-50563.d': (True, True),
            'runs/2013/7/475/sweep_475-50563.d/DATA.MS': (False, False),
            'runs/2013/7/475/sweep_475-50563.d/GC.ini': (False, False),
            'runs/2013/7/475/sweep_475-50563.d/PRE_POST.INI': (False, False),
            'runs/2013/7/475/sweep_475-50563.d/acqmeth.txt': (False, True),
            'runs/2013/7/475/sweep_475-50563.d/cnorm.ini': (False, False),
            'runs/2013/7/475/sweep_475-50563.d/runstart.txt': (False, False),
            'runs/2013/7/475/sweep_475-50563.d/tic_front.csv': (False, False)
            }

        culled = MSDSImpl.cull_empty_dirs(changes)
        culled_files = [f for f, c in culled]
        self.assertTrue("runs/2013" in culled_files)
        self.assertFalse("runs/2013/7/475/solvent_475-50479.d" in culled_files)
        self.assertTrue("runs/2013/7/475/sweep_475-50563.d" in culled_files)
        self.assertTrue("runs/2013/7/475/sweep_475-50563.d/DATA.MS" in culled_files)
        self.assertTrue("runs/2013/7/475/sweep_475-50563.d/acqmeth.txt" in culled_files)
