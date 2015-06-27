# -*- coding: utf-8 -*-
from django.test import TestCase, LiveServerTestCase
from django.test.utils import override_settings
from django.conf import settings
from mastrms.users.models import User
from mastrms.mdatasync_server.models import *
from mastrms.repository.models import *
from mastrms.repository.runbuilder import RunBuilder
from mastrms.testutils import *
from mdatasync_client.Simulator import Simulator
import tempfile
import time
import logging
import os
import pipes
import re
import dingus
from contextlib import contextmanager

logger = logging.getLogger(__name__)

TESTING_REPO = tempfile.mkdtemp(prefix="testrepo-")
logger.info("Created testing repo %s" % TESTING_REPO)

def tearDownModule():
    global TESTING_REPO
    logger.info("Removing testing repo %s" % TESTING_REPO)
    os.rmdir(TESTING_REPO)


@override_settings(REPO_FILES_ROOT=TESTING_REPO)
class DeleteTempFilesTests(TestCase):
    """
    Tests the delete_temp_files management command.
    Todo:
    1. test permissions problems (chmod 000 directory)
    2. test symlinks in tree (shouldn't be followed)
    """

    def setUp(self):
        self.experiments = ["experiment1", "experiment2", "experiment2/subdir",
                            "experiment3"]
        self.worklist = ["runsample1_filename", "runsample2_filename",
                         "teststuff1.d", "teststuff2.d"]

        self.experiments.sort()

        def cleanup_experiments():
            self.experiments.sort(reverse=True)
            for exp in self.experiments:
                try:
                    os.rmdir(os.path.join(TESTING_REPO, exp))
                except OSError:
                    logger.exception("tearDown rmdir")

        self.addCleanup(cleanup_experiments)

        self.temp_files = []
        istemp = lambda f: "TEMP" in f

        for exp in self.experiments:
            destdir = os.path.join(TESTING_REPO, exp)
            os.makedirs(destdir)
            simulator = Simulator(destdir, temp_files=True)
            self.addCleanup(simulator.cleanup)
            simulator.process_worklist(self.worklist)

            self.temp_files.extend(filter(istemp, simulator._created_files))
            self.temp_files.extend(filter(istemp, simulator._created_dirs))

    def test_delete_temp_files(self):
        for f in self.temp_files:
            self.assertTrue(os.path.exists(f), "%s exists" % f)

        from django.core.management import call_command
        call_command("delete_temp_files")

        for f in self.temp_files:
            self.assertFalse(os.path.exists(f), "%s doesn't exist" % f)
