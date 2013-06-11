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
import dingus
from contextlib import contextmanager

def south_shut_up():
    "make south shut up"
    import south.logger
    logging.getLogger('south').setLevel(logging.CRITICAL)

south_shut_up()

@override_settings(REPO_FILES_ROOT=tempfile.mkdtemp(prefix="testrepo"))
class MyFirstSyncTest(LiveServerTestCase):
    # fixme: may be better to use json than setup test case by hand.
    # For some reason, fixtures are required, or else the test case
    # won't find them.
    fixtures = ['mastrms/repository/fixtures/reference_data.json']

    def setUp(self):
        south_shut_up()
        self.setup_more_fixtures()

        if not os.environ.get("DISPLAY"):
            self.use_xvfb()

    def use_xvfb(self):
        from xvfbwrapper import Xvfb
        self.vdisplay = Xvfb()
        self.vdisplay.start()
        self.addCleanup(self.vdisplay.stop)

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

    def test_fixture_setup(self):
        self.assertEquals(self.run.runsample_set.count(), 2)

    def setup_client(self):
        self.worklist = WorkList(get_csv_worklist_from_run(self.run, self.user))

        self.simulator = Simulator()

        logfile = tempfile.NamedTemporaryFile()
        archivedir = tempfile.mkdtemp()

        config = MSDSConfig(user=os.environ["LOGNAME"],
                            sitename=self.nc.site_name,
                            stationname=self.nc.station_name,
                            organisation=self.nc.organisation_name,
                            localdir=self.simulator.destdir,
                            synchub="%s/sync/" % self.live_server_url,
                            logfile=logfile.name,
                            loglevel=plogging.LoggingLevels.DEBUG,
                            archivesynced=True,
                            archivedfilesdir=archivedir)

        test_client = TestClient(config)
        self.test_client = test_client

        return test_client

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
                logger.debug("sleeping")
                time.sleep(4)
                logger.debug("finished")

                self.test_client.quit()

                # load up received json object
                self.assertEquals(len(received_json), 1)
                requested_files = sorted(received_json[0]["files"].keys())

                # a. check that files are requested
                self.assertEquals(len(requested_files), 2)
                self.assertEquals(requested_files[0], "runsample1_filename")
                self.assertEquals(requested_files[1], "runsample2_filename")

                # b. check that rsync was not called
                self.assertEquals(len(subprocess.Popen.calls), 0)

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
                logger.debug("sleeping")
                time.sleep(4)
                logger.debug("finished")

                self.test_client.quit()

                # load up received json object
                logger.debug("received json is %s" % repr(received_json))
                requested_files = [sorted(r["files"].keys()) for r in received_json
                                   if "files" in r]
                self.assertEquals(len(requested_files), 1)

                # a. check that files are requested
                self.assertEquals(len(requested_files[0]), 2)
                self.assertEquals(requested_files[0][0], "runsample1_filename")
                self.assertEquals(requested_files[0][1], "runsample2_filename")

            # b. check that rsync was called
            self.assertEquals(len(rsync_results), 1)
            self.assertTrue(bool(rsync_results[0]))
            # b. check that the file was rsynced
            self.assertEquals(len(rsync_results[0]["source_files"]), 1)
            self.assertEquals(os.path.basename(rsync_results[0]["source_files"][0][1]),
                              "runsample1_filename")

            # c. check server for file
            server_filename = os.path.join(settings.REPO_FILES_ROOT, "runs",
                                           str(self.run.created_on.year),
                                           str(self.run.created_on.month),
                                           str(self.run.id),
                                           "runsample1_filename")
            # fixme: there should be a method on mastrms.repository.Run
            # to get its directory ^^^
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
                logger.debug("sleeping")
                time.sleep(4)

                logger.debug("clicking sync again")
                self.test_client.click_sync()
                logger.debug("sleeping")
                time.sleep(4)

                logger.debug("finished")

                self.test_client.quit()

                # load up received json object
                logger.debug("received json is %s" % repr(received_json))
                requested_files = [sorted(r["files"].keys()) for r in received_json
                                   if "files" in r]
                self.assertEquals(len(requested_files), 2)

                # a. check that 2 files are requested the first sync,
                # then 1 first is requested for second sync.
                self.assertEquals(len(requested_files[0]), 2)
                self.assertEquals(len(requested_files[1]), 1)
                self.assertEquals(requested_files[0][0], "runsample1_filename")
                self.assertEquals(requested_files[0][1], "runsample2_filename")
                self.assertEquals(requested_files[1][0], "runsample2_filename")

            # b. check that rsync was called only once
            self.assertEquals(len(rsync_results), 1)
            self.assertTrue(bool(rsync_results[0]))
            # b. check that the file was rsynced
            self.assertEquals(len(rsync_results[0]["source_files"]), 1)
            self.assertEquals(os.path.basename(rsync_results[0]["source_files"][0][1]),
                              "runsample1_filename")

            # c. check server for file
            server_filename = os.path.join(settings.REPO_FILES_ROOT, "runs",
                                           str(self.run.created_on.year),
                                           str(self.run.created_on.month),
                                           str(self.run.id),
                                           "runsample1_filename")
            # fixme: there should be a method on mastrms.repository.Run
            # to get its directory ^^^
            logger.debug("server filename is %s" % server_filename)
            self.assertTrue(os.path.exists(server_filename))

    def tearDown(self):
        # if self.test_client:
        #     self.test_client.quit()
        pass

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
