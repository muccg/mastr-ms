# -*- coding: utf-8 -*-
import os
from django.utils import unittest
from django.test.utils import override_settings
from django.test import TestCase, LiveServerTestCase
from nose.plugins.attrib import attr
import dingus
import tempfile
import logging
from contextlib import contextmanager

from mastrms.testutils import *

from mdatasync_client.Simulator import Simulator, WorkList
from mdatasync_client.test import TestClient, FakeRsync
from mdatasync_client.config import MSDSConfig, plogging
from mdatasync_client import plogging

TESTING_REPO = tempfile.mkdtemp(prefix="testrepo-")
logger = logging.getLogger(__name__)
logger.info("Created testing repo %s" % TESTING_REPO)

def tearDownModule():
    global TESTING_REPO
    logger.info("Removing testing repo %s" % TESTING_REPO)
    os.rmdir(TESTING_REPO)


@attr("synctest", "xdisplay")
@override_settings(REPO_FILES_ROOT=TESTING_REPO)
class SyncTests(LiveServerTestCase, XDisplayTest, WithFixtures):
    def setUp(self):
        self.test_client = None
        self.setup_more_fixtures()
        self.setup_display()
        return super(SyncTests, self).setUp()

    def tearDown(self):
        # clean out the temporary dir
        logger.info("Clearing out testing repo %s" % pipes.quote(settings.REPO_FILES_ROOT))
        for f in os.listdir(settings.REPO_FILES_ROOT):
            os.system("rm -rf %s" % pipes.quote(os.path.join(settings.REPO_FILES_ROOT, f)))

    @classmethod
    def setUpClass(cls):
        #cls.setup_display()
        super(SyncTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        #cls.teardown_display()
        super(SyncTests, cls).tearDownClass()

    def test_sync1(self):
        "1. add a run, with 2 or more samples"
        self.assertEqual(self.run.runsample_set.count(), 2)

    def setup_client(self, **extra_config):
        """
        Creates a test client, CSV worklist, simulator, and the
        necessary data directories.
        Everything will be cleaned up when the test case is torn down.
        Default test config parameters can be overridden with keyword
        arguments.
        """

        self.worklist = WorkList(get_csv_worklist_from_run(self.run, self.user))

        self.simulator = Simulator()
        self.addCleanup(self.simulator.cleanup)

        logfile = tempfile.NamedTemporaryFile(prefix="rsync-", suffix=".log")
        archivedir = tempfile.mkdtemp(prefix="archive-")

        config = MSDSConfig(user=self.user,
                            sitename=self.nc.site_name,
                            stationname=self.nc.station_name,
                            organisation=self.nc.organisation_name,
                            localdir=unicode(self.simulator.destdir),
                            synchub="%s/sync/" % 'http://web:8000',
                            logfile=logfile.name,
                            loglevel=plogging.LoggingLevels.DEBUG,
                            archivesynced=False,
                            archivedfilesdir=archivedir)

        config.update(extra_config)

        test_client = TestClient(config, timeout=120, maximize=True)
        test_client.set_window_title(self.id())
        self.test_client = test_client

        self.addCleanup(self.cleanup_client_files)
        self.addCleanup(test_client.quit)

        return test_client

    def cleanup_client_files(self):
        config = self.test_client.config
        try: os.remove(config["logfile"])
        except EnvironmentError: pass
        try: os.system("rm -rf %s" % pipes.quote(config["archivedfilesdir"]))
        except EnvironmentError: pass

    def test_sync2(self):
        """
        We are testing for Popen calls to check how rsync was
        called. Maybe it would be better to create a mock rsync
        command and put it in the PATH.
        """
        import subprocess
        with dingus.patch("subprocess.Popen"):
            self.setup_client()

            # Start recording json received from server
            received_json = []
            with json_hooker(received_json):
                # Initiate sync
                logger.debug("about to click_sync")
                self.test_client.click_sync()
                logger.debug("finished")

                self.test_client.quit()

                # load up received json object
                self.assertEqual(len(received_json), 1)
                requested_files = self.find_files_in_json(received_json)[0]

                # a. check that files are requested
                self.assertEqual(len(requested_files), 2)
                self.assertEqual(requested_files[0], "runsample1_filename")
                self.assertEqual(requested_files[1], "runsample2_filename")

                # b. check that rsync was not called
                self.assertEqual(len(subprocess.Popen.calls), 0)

        self.assertTrue(True)


    def test_sync3(self):
        rsync_results = []
        with FakeRsync(rsync_results, do_copy=True):
            self.setup_client()

            logger.debug("worklist is %s" % str(self.worklist))
            # Add a file to the client data folder
            self.simulator.process_worklist(self.worklist[0:1])

            # Start recording json received from server
            with json_hooker() as received_json:
                # Initiate sync
                logger.debug("about to click_sync")
                self.test_client.click_sync()
                logger.debug("finished")

                self.test_client.quit()

                # load up received json object
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 1)

                # a. check that files are requested
                self.assertEqual(len(requested_files[0]), 2)
                self.assertEqual(requested_files[0][0], "runsample1_filename")
                self.assertEqual(requested_files[0][1], "runsample2_filename")

            # b. check that rsync was called
            self.assertEqual(len(rsync_results), 1)
            self.assertTrue(bool(rsync_results[0]))
            # b. check that the file was rsynced
            self.assertEqual(len(rsync_results[0]["source_files"]), 1)
            self.assertEqual(os.path.basename(rsync_results[0]["source_files"][0][1]),
                              "runsample1_filename")

            # c. check server for file
            server_filename = runsample_filename(self.run, "runsample1_filename")
            logger.debug("server filename is %s" % server_filename)
            self.assertTrue(os.path.exists(server_filename))

    def test_sync4(self):
        rsync_results = []
        with FakeRsync(rsync_results, do_copy=True):
            self.setup_client()

            # Add a file to the client data folder
            self.simulator.process_worklist(self.worklist[0:1])

            # Start recording json received from server
            with json_hooker() as received_json:
                # Initiate sync
                logger.debug("about to click_sync")
                self.test_client.click_sync()

                logger.debug("clicking sync again")
                self.test_client.click_sync()

                logger.debug("clicking sync a third time")
                self.test_client.click_sync() # rsync should not be run here

                logger.debug("finished")

                self.test_client.quit()

                # load up received json object
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 3,
                                 "three requested files responses")

                # a. check that 2 files are requested the first sync,
                # then 2 are requested for second sync,
                # then 1 file is requested for the third sync
                self.assertEqual(len(requested_files[0]), 2,
                                 "2 files are requested the first sync")
                self.assertEqual(len(requested_files[1]), 2,
                                 "2 files are requested for second sync")
                self.assertEqual(len(requested_files[2]), 1,
                                 "1 file is requested for third sync")
                self.assertEqual(requested_files[0][0], "runsample1_filename")
                self.assertEqual(requested_files[0][1], "runsample2_filename")
                self.assertEqual(requested_files[1][0], "runsample1_filename")
                self.assertEqual(requested_files[1][1], "runsample2_filename")
                self.assertEqual(requested_files[2][0], "runsample2_filename")

            # b. check that rsync was called twice
            self.assertEqual(len(rsync_results), 2,
                             "check that rsync was called twice")
            self.assertTrue(bool(rsync_results[0]))
            self.assertTrue(bool(rsync_results[1]))
            # b. check that the file was rsynced
            self.assertEqual(len(rsync_results[0]["source_files"]), 1)
            self.assertEqual(os.path.basename(rsync_results[0]["source_files"][0][1]),
                             "runsample1_filename",
                             "first rsync transfers file 1")
            self.assertEqual(len(rsync_results[1]["source_files"]), 1)
            self.assertEqual(os.path.basename(rsync_results[1]["source_files"][0][1]),
                             "runsample1_filename",
                             "second rsync transfers file 1")

            # c. check server for file
            server_filename = runsample_filename(self.run, "runsample1_filename")
            logger.debug("server filename is %s" % server_filename)
            self.assertTrue(os.path.exists(server_filename),
                            "%s exists on server" % server_filename)

            # d. check sample completion status
            samples = self.run.runsample_set.order_by("filename")
            self.assertTrue(samples[0].complete,
                            "First sample %s is marked complete" % samples[0].filename)
            self.assertFalse(samples[1].complete,
                             "Second sample %s is not marked complete" % samples[1].filename)
            self.assertNotEqual(self.run.state, RUN_STATES.COMPLETE[0],
                                "Run is not marked complete")

    def test_sync5(self):
        rsync_results = []
        with FakeRsync(rsync_results, do_copy=True):
            self.setup_client()

            # Add a file to the client data folder
            self.simulator.process_worklist(self.worklist[0:1])

            with json_hooker() as received_json:
                logger.debug("about to click_sync")
                self.test_client.click_sync()
                logger.debug("clicking sync again")
                self.test_client.click_sync()

                # load up received json object
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 2)

                # a. check that 2 files are requested the first sync,
                # then 2 files are requested for second sync.
                self.assertEqual(len(requested_files[0]), 2,
                                 "2 files are requested the first sync")
                self.assertEqual(len(requested_files[1]), 2,
                                 "2 files are requested for second sync")
                self.assertEqual(requested_files[0][0], "runsample1_filename")
                self.assertEqual(requested_files[0][1], "runsample2_filename")
                self.assertEqual(requested_files[1][0], "runsample1_filename")

                # clear received json for testing purposes
                del received_json[:]

                # Add another file to the client data folder
                self.simulator.process_worklist(self.worklist[1:2])
                self.test_client.click_sync()

                logger.debug("finished")
                self.test_client.quit()

                # Check that 1 file is still requested
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 1)

            self.assertEqual(len(rsync_results), 3,
                             "check that rsync was called three times")
            self.assertTrue(bool(rsync_results[0]))
            self.assertTrue(bool(rsync_results[1]))
            self.assertTrue(bool(rsync_results[2]))
            # b. check that the file was rsynced
            self.assertEqual(len(rsync_results[0]["source_files"]), 1,
                             "first rsync transfers 1 file")
            self.assertEqual(os.path.basename(rsync_results[0]["source_files"][0][1]),
                             "runsample1_filename",
                             "first rsync transfers file 1")
            self.assertEqual(len(rsync_results[1]["source_files"]), 1,
                             "second rsync transfers 1 file")
            self.assertEqual(os.path.basename(rsync_results[1]["source_files"][0][1]),
                             "runsample1_filename",
                             "second rsync transfers file 1")
            self.assertEqual(len(rsync_results[2]["source_files"]), 1,
                             "third rsync transfers 1 file")
            self.assertEqual(os.path.basename(rsync_results[2]["source_files"][0][1]),
                             "runsample2_filename",
                             "third rsync transfers file 2")

            # c. check server for presence of files
            server_filename = runsample_filename(self.run, "runsample1_filename")
            logger.debug("server filename 1 is %s" % server_filename)
            self.assertTrue(os.path.exists(server_filename))
            server_filename = runsample_filename(self.run, "runsample2_filename")
            logger.debug("server filename 2 is %s" % server_filename)
            self.assertTrue(os.path.exists(server_filename))

    def test_sync6(self):
        rsync_results = []
        with FakeRsync(rsync_results, do_copy=True):
            self.setup_client()

            # Add a file to the client data folder
            self.simulator.process_worklist(self.worklist[0:1])

            with json_hooker() as received_json:
                logger.debug("about to click_sync")
                self.test_client.click_sync()
                logger.debug("clicking sync again")
                self.test_client.click_sync()
                logger.debug("clicking sync once more")
                self.test_client.click_sync() # this shouldn't result in an rsync

                # load up received json object
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 3,
                                 "three requested files responses")

                # a. check that 2 files are requested the first sync,
                # then 2 are is requested for second sync,
                # then 1 is requested for the third sync
                self.assertEqual(len(requested_files[0]), 2,
                                 "2 files are requested the first sync")
                self.assertEqual(len(requested_files[1]), 2,
                                 "2 files are requested for second sync")
                self.assertEqual(len(requested_files[2]), 1,
                                 "1 file is requested for third sync")
                self.assertEqual(requested_files[0][0], "runsample1_filename")
                self.assertEqual(requested_files[0][1], "runsample2_filename")
                self.assertEqual(requested_files[1][0], "runsample1_filename")
                self.assertEqual(requested_files[1][1], "runsample2_filename")
                self.assertEqual(requested_files[2][0], "runsample2_filename")

                # clear received json for testing purposes
                del received_json[:]

                # Add another file to the client data folder, do sync
                self.simulator.process_worklist(self.worklist[1:2])
                self.test_client.click_sync()

                # Check that 1 file is still requested
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 1,
                                 "check that 1 file is still requested")

                # clear received json for testing purposes
                del received_json[:]

                # append data to a files on client, do sync
                self.simulator.add_more_data_with_worklist(self.worklist[0:2])
                self.test_client.click_sync()

                # Check that 1 file is still requested
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 1,
                                 "check that 1 file is still requested")

                logger.debug("finished")
                self.test_client.quit()


            # b. check that rsync was called four times
            self.assertEqual(len(rsync_results), 4,
                             "check that rsync was called five times")
            self.assertTrue(bool(rsync_results[0]))
            self.assertTrue(bool(rsync_results[1]))
            self.assertTrue(bool(rsync_results[2]))
            self.assertTrue(bool(rsync_results[3]))
            # b. check that both files were rsynced
            self.assertEqual(len(rsync_results[0]["source_files"]), 1)
            self.assertEqual(os.path.basename(rsync_results[0]["source_files"][0][1]),
                             "runsample1_filename",
                             "first rsync transfers file 1")
            self.assertEqual(len(rsync_results[1]["source_files"]), 1)
            self.assertEqual(os.path.basename(rsync_results[1]["source_files"][0][1]),
                             "runsample1_filename",
                             "second rsync transfers file 1")
            self.assertEqual(len(rsync_results[1]["source_files"]), 1)
            self.assertEqual(os.path.basename(rsync_results[2]["source_files"][0][1]),
                             "runsample2_filename",
                             "third rsync transfers file 2")
            self.assertEqual(os.path.basename(rsync_results[3]["source_files"][0][1]),
                             "runsample2_filename",
                             "fourth rsync transfers file 2")

            # c. check server for presence of files
            server_filename = runsample_filename(self.run, "runsample1_filename")
            logger.debug("server filename 1 is %s" % server_filename)
            self.assertTrue(os.path.exists(server_filename),
                            "%s exists on server" % server_filename)
            server_filename = runsample_filename(self.run, "runsample2_filename")
            logger.debug("server filename 2 is %s" % server_filename)
            self.assertTrue(os.path.exists(server_filename),
                            "%s exists on server" % server_filename)

    def test_sync7(self):
        rsync_results = []
        with FakeRsync(rsync_results, do_copy=True):
            self.setup_client()

            # Add files to the client data folder
            self.simulator.process_worklist(self.worklist[0:2])

            with json_hooker() as received_json:
                # sync across files, have them marked as complete
                logger.debug("doing double sync")
                self.test_client.click_sync()
                self.test_client.click_sync()

                # load up received json object
                requested_files = self.find_files_in_json(received_json)
                self.assertEqual(len(requested_files), 2,
                                 "two requested files responses")
                # a. check that 2 files are requested the first sync,
                # then 2 are is requested for second sync,
                # then 1 is requested for the third sync
                self.assertEqual(len(requested_files[0]), 2,
                                 "2 files are requested the first sync")
                self.assertEqual(len(requested_files[1]), 2,
                                 "2 files are requested for second sync")
                self.assertEqual(requested_files[0][0], "runsample1_filename")
                self.assertEqual(requested_files[0][1], "runsample2_filename")
                self.assertEqual(requested_files[1][0], "runsample1_filename")
                self.assertEqual(requested_files[1][1], "runsample2_filename")

                # refresh the stored run object
                self.run = Run.objects.get(pk=self.run.pk)

                # check sample completion status in db
                rs = self.run.runsample_set.order_by("filename")
                self.assertSequenceEqual(rs.values_list("complete", flat=True),
                                         [True, True],
                                         "Check that RunSamples are marked complete")
                self.assertEqual(self.run.state, RUN_STATES.COMPLETE[0],
                                 "Run is marked complete")

                # clear received json for testing purposes
                del received_json[:]

                # mark the samples as incomplete
                self.run.runsample_set.update(complete=False)
                self.run.state = RUN_STATES.IN_PROGRESS[0]
                self.run.save()

                logger.debug("clicking sync again")
                self.test_client.click_sync()

                # load up received json object
                requested_files = self.find_files_in_json(received_json)

                self.assertEqual(len(requested_files), 1)
                self.assertEqual(len(requested_files[0]), 2,
                                 "2 files are requested")
                self.assertEqual(requested_files[0][0], "runsample1_filename")
                self.assertEqual(requested_files[0][1], "runsample2_filename")

                logger.debug("finished")
                self.test_client.quit()


            # b. check that files are rsynced
            self.assertEqual(len(rsync_results), 3,
                             "check that rsync was called three times")
            self.assertTrue(bool(rsync_results[0]))
            self.assertTrue(bool(rsync_results[1]))
            self.assertTrue(bool(rsync_results[2]))
            # b. check that both files were rsynced
            self.assertListEqual([os.path.basename(f[1]) for f in rsync_results[0]["source_files"]],
                                 ["runsample1_filename", "runsample2_filename"],
                                 "first rsync transfers both files")
            self.assertListEqual([os.path.basename(f[1]) for f in rsync_results[1]["source_files"]],
                                 ["runsample1_filename", "runsample2_filename"],
                                 "second rsync transfers both files")
            self.assertListEqual([os.path.basename(f[1]) for f in rsync_results[2]["source_files"]],
                                 ["runsample1_filename", "runsample2_filename"],
                                 "third rsync transfers both files")

            # c. check server for presence of files
            server_filename = runsample_filename(self.run, "runsample1_filename")
            self.assertFileExists(server_filename)
            self.assertTrue(os.path.exists(server_filename),
                            "%s exists on server" % server_filename)
            server_filename = runsample_filename(self.run, "runsample2_filename")
            self.assertFileExists(server_filename)
            self.assertTrue(os.path.exists(server_filename),
                            "%s exists on server" % server_filename)

    def test_sync8(self):
        """
        Check that TEMP files generated by simulator aren't rsynced by
        the client.
        """

        # change the first sample so it is created as a directory
        rs = self.run.runsample_set.order_by("filename")[0]
        rs.filename = "runsample1_filename.d"
        rs.save()

        with FakeRsync(do_copy=True) as rsync_results:
            self.setup_client()

            # Add files to the client data folder,
            # with TEMP files mixed in
            worklist = ["runsample1_filename.d", "runsample2_filename",
                        "teststuff1.d", "teststuff2.d"]
            worklist = [os.path.join("experiments/2013/my test experiment", f)
                        for f in worklist]
            self.simulator.generate_temp_files = True
            self.simulator.process_worklist(worklist)

            # do the sync
            self.test_client.click_sync()
            self.test_client.quit()

            # check that there actually were temp files produced by
            # simulator
            temps = filter(Simulator.istemp, self.simulator.created_files)
            self.assertNotEqual(len(temps), 0, "temp files created")

            # check the files in the rsync src dir
            self.assertEqual(len(rsync_results), 1)
            istemp = lambda (srcdir, path): Simulator.istemp(path)
            temps = filter(istemp, rsync_results[0]["source_files"])
            self.assertEqual(len(temps), 0, "no temp files rsynced")

    def test_sync9(self):
        """
        Tests that empty directories aren't marked as complete.
        """
        rsync_results = []
        with FakeRsync(rsync_results, do_copy=True):
            self.setup_client()

            # Add an empty directory to the client data folder
            test_directory = os.path.join(self.simulator.destdir, self.worklist[0])
            os.mkdir(test_directory)
            self.addCleanup(os.rmdir, test_directory)

            # Start recording json received from server
            with json_hooker() as received_json:
                # Initiate sync
                logger.debug("about to click_sync")
                self.test_client.click_sync()

                logger.debug("clicking sync again")
                self.test_client.click_sync()

                logger.debug("finished")

                self.test_client.quit()

            # b. check that rsync was called twice
            self.assertEqual(len(rsync_results), 2,
                             "check that rsync was called twice")
            self.assertTrue(bool(rsync_results[0]))
            self.assertTrue(bool(rsync_results[1]))
            # b. check that nothing was rsynced
            self.assertEqual(len(rsync_results[0]["source_files"]), 0)
            self.assertEqual(len(rsync_results[1]["source_files"]), 0)

            # c. check server for directory
            server_filename = runsample_filename(self.run, self.worklist[0])
            self.assertFalse(os.path.exists(server_filename),
                            "%s doesn't exist on server" % server_filename)

            # d. check sample completion status
            samples = self.run.runsample_set.order_by("filename")
            self.assertFalse(samples[0].complete,
                             "First sample %s is not marked complete" % samples[0].filename)

    class FileDoesNotExistAssertion(AssertionError):
        pass
    class FileExistsAssertion(AssertionError):
        pass
    def assertFileExists(self, filename, msg=None):
        if not os.path.exists(filename):
            msg = msg or "%s exists" % filename
            raise FileDoesNotExistAssertion, msg
    def assertFileDoesNotExist(self, filename, msg=None):
        if os.path.exists(filename):
            msg = msg or "%s doesn't exist" % filename
            raise FileExistsAssertion, msg

    def test_unicode1(self):
        """
        Tests connecting to a station with unicode characters in its name.
        """

        # capture log messages from client
        handler = MockLoggingHandler()
        logging.getLogger("client").addHandler(handler)

        self.nc.organisation_name = u"org ☃"
        self.nc.site_name = u"site λ"
        self.nc.station_name = u"station µ"
        self.nc.save()

        with FakeRsync():
            self.setup_client()

            # Add a file to the client data folder
            self.simulator.process_worklist(self.worklist[0:1])

            with json_hooker() as received_json:
                self.test_client.click_sync()

                # check that the request was made
                requested_files = self.find_files_in_json(received_json)

                self.assertEqual(len(requested_files), 1)

                # a. check that files are requested
                self.assertEqual(len(requested_files[0]), 2)
                self.assertEqual(requested_files[0][0], "runsample1_filename")
                self.assertEqual(requested_files[0][1], "runsample2_filename")

    @staticmethod
    def hack_unicode_filenames(runsamples):
        """
        I was unable to figure out how the rule generators, sample
        blocks, etc worked, so couldn't get unicode filenames in the
        normal way.
        This method forces the RunSample filenames to be unicode.
        """
        for rs in runsamples:
            d, f = os.path.split(rs.filename)
            fs = f.split("_")
            fs[0] = u"unicode test µ"
            rs.filename = os.path.join(d, "_".join(fs))
            rs.save()

    def test_unicode2(self):
        """
        Test that syncing doesn't bomb when the unicode sample
        filenames have non-ascii characters.
        """
        Sample.objects.update(label=u"labelµ")

        rb = RunBuilder(self.run)
        rb.generate()

        self.hack_unicode_filenames(self.run.runsample_set.all())
        self.worklist = WorkList(get_csv_worklist_from_run(self.run, self.user))

        with FakeRsync():
            self.setup_client()

            # Add a file to the client data folder
            self.simulator.process_worklist(self.worklist[0:1])

            with json_hooker() as received_json:
                self.test_client.click_sync()

    def test_unicode3(self):
        """
        this test doesn't work.
        """
        #self.sample.sample_class.class_id = u"⌨"
        #self.sample.sample_class.save()
        SampleClass.objects.update(class_id=u"⌨")

        rb = RunBuilder(self.run)
        rb.generate()

        with FakeRsync():
            self.setup_client()

            # Add a file to the client data folder
            self.simulator.process_worklist(self.worklist[0:1])

            with json_hooker() as received_json:
                self.test_client.click_sync()


    @staticmethod
    def find_files_in_json(received_json):
        """
        Looks in the captured json dicts for objects with contain
        "files" and returns these values.
        Returns a list of lists -- a list for each request.
        """
        logger.debug("received json is %s" % repr(received_json))
        return [sorted(r["files"].keys())
                for r in received_json
                if "files" in r]

@contextmanager
def json_hooker(received_json=None):
    "Overrides json.loads() to record objects received from the server."
    if received_json is None:
        received_json = []
    logger.debug("hooking into json")
    import json
    old_loads = json.loads
    def loads_parasite(*args, **kwargs):
        logger.debug("parasite loads: %s" % args[0])
        ob = old_loads(*args, **kwargs)
        received_json.append(ob)
        return ob
    json.loads = loads_parasite
    yield received_json
    json.loads = old_loads

def get_csv_worklist_from_run(run, user):
    """
    In the datasync server, csv worklist is generated through a
    template, so it can't be reused => reimplement it here.
    """
    def csv_line(sample):
        return ",".join(map(unicode, [
                        user,
                        run.machine.default_data_path,
                        sample.filename,
                        run.method.method_path,
                        run.method.method_name,
                        sample.sample_name
                        ]))
    runsamples = run.runsample_set.order_by("sequence", "filename")
    return "\n".join(map(csv_line, runsamples)) + "\n"

def runsample_filename(run, sample_filename):
    """
    Gets the absolute expected filename for a runsample.
    fixme: there should be a method on mastrms.repository.Run
           to get its directory.
    """
    return os.path.join(settings.REPO_FILES_ROOT, "runs",
                        str(run.created_on.year),
                        str(run.created_on.month),
                        str(run.id), sample_filename)
