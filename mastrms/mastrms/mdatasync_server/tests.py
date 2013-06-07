from django.test import TestCase, LiveServerTestCase
from mastrms.mdatasync_server.models import *
from mastrms.repository.models import *
from mastrms.mdatasync_client.client.Simulator import Simulator
from mastrms.mdatasync_client.client.test import TestClient
from mastrms.mdatasync_client.client.config import MSDSConfig, plogging
import tempfile
import mastrms.mdatasync_client.client.plogging  # wtf
import time
import logging

def south_shut_up():
    "make south shut up"
    import south.logger
    logging.getLogger('south').setLevel(logging.CRITICAL)

south_shut_up()

class MyFirstSyncTest(LiveServerTestCase):
    # fixme: may be better to use json than setup test case by hand.
    # For some reason, fixtures are required, or else the test case
    # won't find them.
    fixtures = ['mastrms/repository/fixtures/reference_data.json']

    def setUp(self):
        south_shut_up()

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
        # runsample2 = RunSample.objects.create(run=run, sample=sample,
        #                                       component=sb)

        self.user = user
        self.nc = nc
        self.run = run
        self.test_client = None

    def test_something(self):
        self.assertEquals(self.run.runsample_set.count(), 1)

        worklist = get_csv_worklist_from_run(self.run, self.user)

        simulator = Simulator()

        logfile = tempfile.NamedTemporaryFile()
        archivedir = tempfile.mkdtemp()

        config = MSDSConfig(user=os.environ["LOGNAME"],
                            sitename=self.nc.site_name,
                            stationname=self.nc.station_name,
                            organisation=self.nc.organisation_name,
                            localdir=simulator.destdir,
                            synchub="%s/sync/" % self.live_server_url,
                            logfile=logfile.name,
                            loglevel=plogging.LoggingLevels.DEBUG,
                            archivesynced=True,
                            archivedfilesdir=archivedir)

        test_client = TestClient(config)
        self.test_client = test_client

        logger.debug("about to click_sync")
        self.test_client.click_sync()
        logger.debug("sleeping")
        time.sleep(10)
        logger.debug("finished")

        self.test_client.quit()

        self.assertTrue(True)

    def tearDown(self):
        # if self.test_client:
        #     self.test_client.quit()
        pass

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

    return "\n".join(map(csv_line, run.runsample_set.order_by("sequence"))) + "\n"


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
