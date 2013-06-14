from django.test import TestCase, LiveServerTestCase
from django.test.utils import override_settings
from django.conf import settings
from mastrms.mdatasync_server.models import *
from mastrms.repository.models import *
from mastrms.mdatasync_client.client.Simulator import Simulator, WorkList
from mastrms.mdatasync_client.client.test import TestClient, FakeRsync
from mastrms.mdatasync_client.client.config import MSDSConfig, plogging
import tempfile
import mastrms.mdatasync_client.client.plogging  # wtf
import time
import logging
import os
import pipes
import dingus
from contextlib import contextmanager

logger = logging.getLogger(__name__)

def south_shut_up():
    "make south shut up"
    import south.logger
    logging.getLogger('south').setLevel(logging.CRITICAL)

south_shut_up()

TESTING_REPO = tempfile.mkdtemp(prefix="testrepo-")
logger.info("Created testing repo %s" % TESTING_REPO)

def tearDownModule():
    global TESTING_REPO
    logger.info("Removing testing repo %s" % TESTING_REPO)
    os.rmdir(TESTING_REPO)

@override_settings(REPO_FILES_ROOT=TESTING_REPO)
class MyFirstSyncTest(LiveServerTestCase):
    # fixme: may be better to use json than setup test case by hand.
    # For some reason, fixtures are required, or else the test case
    # won't find them.
    fixtures = ['mastrms/repository/fixtures/reference_data.json']

    def setUp(self):
        south_shut_up()
        self.setup_more_fixtures()

        self.setup_display()

        return super(MyFirstSyncTest, self).setUp()

    def tearDown(self):
        # clean out the temporary dir
        logger.info("Clearing out testing repo %s" % pipes.quote(settings.REPO_FILES_ROOT))
        for f in os.listdir(settings.REPO_FILES_ROOT):
            os.system("rm -rf %s" % pipes.quote(os.path.join(settings.REPO_FILES_ROOT, f)))

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

    @classmethod
    def setUpClass(cls):
        cls.setup_display()
        super(MyFirstSyncTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.teardown_display()
        super(MyFirstSyncTest, cls).tearDownClass()

    def setup_more_fixtures(self):
        # nodeclient, project, experiment, run, samples
        nc = NodeClient.objects.create(organisation_name="org", site_name="site",
                                       station_name="station",
                                       default_data_path="testing data path",
                                       username=os.environ["LOGNAME"],
                                       flags="-rz")

        #user = User.objects.get(username__istartswith="admin")
        user = User.objects.create(username="testuser")

        project = Project.objects.create(title="Project", description="Test project",
                                         client=user)

        method = InstrumentMethod.objects.create(title="Instrument Method",
                                                 method_path="METHOD_PATH",
                                                 method_name="METHOD_NAME",
                                                 version="", template="",
                                                 creator=user)

        experiment = Experiment.objects.create(title="Test experiment",
                                               description="We're testing to see if this code works",
                                               comment="Maybe it doesn't",
                                               job_number="job_number",
                                               project=project,
                                               instrument_method=method)

        rulegen = RuleGenerator.objects.create(name="Rule Gen", description="test",
                                               created_by=user)

        run = Run.objects.create(experiment=experiment, method=method,
                                 creator=user, machine=nc, state=RUN_STATES.NEW[0],
                                 rule_generator=rulegen)

        biological_source = None
        treatments = None
        timeline = SampleTimeline.objects.create(experiment=experiment,
                                                 abbreviation="st",
                                                 timeline="timeline")
        organ = None

        sclass = SampleClass.objects.create(class_id="CLSID", experiment=experiment,
                                            biological_source=biological_source,
                                            treatments=treatments,
                                            timeline=timeline,
                                            organ=organ)

        sample = Sample.objects.create(sample_id="sid1", sample_class=sclass,
                                       experiment=experiment, label="Sample Label",
                                       comment="Sample comment",
                                       weight="3.1415926535897931")

        pbqc = Component.objects.get(sample_code="pbqc")
        sb = Component.objects.get(sample_code="SB")

        runsample1 = RunSample.objects.create(run=run, sample=sample,
                                              component=pbqc,
                                              filename="runsample1_filename")
        runsample2 = RunSample.objects.create(run=run, sample=sample,
                                              component=sb,
                                              filename="runsample2_filename")

        self.user = user
        self.nc = nc
        self.run = run
        self.test_client = None

    def test_sync1(self):
        # 1. add a run, with 2 or more samples
        self.assertEqual(self.run.runsample_set.count(), 2)

    def setup_client(self):
        self.worklist = WorkList(get_csv_worklist_from_run(self.run, self.user))

        self.simulator = Simulator()
        self.addCleanup(self.simulator.cleanup)

        logfile = tempfile.NamedTemporaryFile(prefix="rsync-", suffix=".log")
        archivedir = tempfile.mkdtemp(prefix="archive-")

        config = MSDSConfig(user=os.environ["LOGNAME"],
                            sitename=self.nc.site_name,
                            stationname=self.nc.station_name,
                            organisation=self.nc.organisation_name,
                            localdir=self.simulator.destdir,
                            synchub="%s/sync/" % self.live_server_url,
                            logfile=logfile.name,
                            loglevel=plogging.LoggingLevels.DEBUG,
                            archivesynced=False,
                            archivedfilesdir=archivedir)

        test_client = TestClient(config, maximize=True)
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
        # We are testing for Popen calls to check how rsync was
        # called. Maybe it would be better to create a mock rsync
        # command and put it in the PATH.
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
        return ",".join(map(str, [
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


# # Trying out selenium tests
# # fixme: maybe use splinter for testing
# # http://splinter.cobrateam.info/
# from django.test import LiveServerTestCase
# from selenium.webdriver.chrome.webdriver import WebDriver

# class MySeleniumTests(LiveServerTestCase):
#     #fixtures = ['user-data.json']

#     @classmethod
#     def setUpClass(cls):
#         cls.selenium = WebDriver()
#         super(MySeleniumTests, cls).setUpClass()

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super(MySeleniumTests, cls).tearDownClass()

#     def test_login(self):
#         self.selenium.get("%s%s" % (self.live_server_url, "/repoadmin/"))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys("admin@example.com")
#         password_input = self.selenium.find_element_by_name("password")
#         password_input.send_keys("admin")
#         self.selenium.find_element_by_xpath("//input[@value='Log in']").click()
