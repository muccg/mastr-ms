import logging
import os
from testcases import NonFlushingTransactionTestCaseMixin
#from mastrms.mdatasync_server.models import NodeClient
from mastrms.repository.models import *
from mastrms.users.models import User

__all__ = ["MockLoggingHandler", "XDisplayTest", "WithFixtures",
           "NonFlushingTransactionTestCaseMixin"]

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


class WithFixtures(object):
    "TestCase mixin to provide fixtures for tests."
    # For some reason, fixtures are required, or else the test case
    # won't find them.
    fixtures = [
        "mastrms/repository/fixtures/reference_data.json",
        ]

    def setup_more_fixtures(self):
        """
        Setup some objects to be used in test cases.

        fixme: may be better to use json than creating them by hand.
        """

        # nodeclient, project, experiment, run, samples
        nc = NodeClient.objects.create(organisation_name="org", site_name="site",
                                       station_name="station",
                                       default_data_path="testing data path",
                                       username='admin',
                                       flags="-rz")

        #user = User.objects.get(email__istartswith="admin")
        #user = User.objects.create(email="testuser", is_staff=True)
        self.admin_password = "admin"
        self.admin = self.create_user("admin@example.com", self.admin_password, True)
        self.user_password = "testing"
        self.user = self.create_user("testuser@ccg.murdoch.edu.au", self.user_password)

        project = Project.objects.create(title="Project", description="Test project",
                                         client=self.user)

        method = InstrumentMethod.objects.create(title="Instrument Method",
                                                 method_path="METHOD_PATH",
                                                 method_name="METHOD_NAME",
                                                 version="", template="",
                                                 creator=self.user)

        experiment = Experiment.objects.create(title="Test experiment",
                                               description="We're testing to see if this code works",
                                               comment="Maybe it doesn't",
                                               job_number="job_number",
                                               project=project,
                                               instrument_method=method)

        rulegen = RuleGenerator.objects.create(name="Rule Gen", description="test",
                                               created_by=self.user,
                                               state=RuleGenerator.STATE_ENABLED,
                                               accessibility=RuleGenerator.ACCESSIBILITY_ALL)

        pbqc = Component.objects.get(sample_code="pbqc")
        sb = Component.objects.get(sample_code="SB")
        smp = Component.objects.get(sample_code="Smp")

        sample_block = RuleGeneratorStartBlock(rule_generator=rulegen, index=1, count=1,
                                              component=pbqc)
        start_block = RuleGeneratorSampleBlock(rule_generator=rulegen, index=2,
                                                sample_count=1, count=1,
                                                component=smp, order=1)
        end_block = RuleGeneratorEndBlock(rule_generator=rulegen, index=3, count=1,
                                          component=sb)
        for block in start_block, sample_block, end_block:
            block.save()

        run = Run.objects.create(experiment=experiment, method=method,
                                 creator=self.user, machine=nc, state=RUN_STATES.NEW[0],
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

        runsample1 = RunSample.objects.create(run=run, sample=sample,
                                              component=pbqc,
                                              filename="runsample1_filename")
        runsample2 = RunSample.objects.create(run=run, sample=sample,
                                              component=sb,
                                              filename="runsample2_filename")

        self.nc = nc
        self.sample = sample
        self.run = Run.objects.get(id=run.id)

    def create_user(self, email, password="test", is_admin=True):
        """
        Creates a django user and returns it.
        """
        user = User.objects.filter(email=email)
        if user.exists():
            user = user[0]
        else:
            user = User(email=email)
        user.set_password(password)
        user.save()
        user.IsAdmin = is_admin
        user.save()
        return user
