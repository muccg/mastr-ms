import os
import os.path
from django.core.management.base import BaseCommand, CommandError
from mastrms.mdatasync_server.models import NodeClient
from mastrms.repository.models import RunSample
from django.conf import settings

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Deletes TEMP files which were uploaded by an older datasync client.'

    VICTIMS = ["TEMPBASE", "TEMPDAT", "TEMPDIR"]

    def handle(self, *args, **options):
        logger.info("*** Processing %s ***" % settings.REPO_FILES_ROOT)

        num_files = 0
        num_dirs = 0
        num_errors = 0

        for root, dirs, files in os.walk(settings.REPO_FILES_ROOT, topdown=False):

            for name in files:
                if name in self.VICTIMS:
                    path = os.path.join(root, name)
                    try:
                        logger.info("Deleting file %s" % path)
                        os.remove(path)
                        num_files += 1
                    except EnvironmentError as e:
                        logger.error(e)
                        num_errors += 1

            for name in dirs:
                if name in self.VICTIMS:
                    path = os.path.join(root, name)
                    try:
                        logger.info("Deleting directory %s" % path)
                        os.rmdir(path)
                        num_dirs += 1
                    except EnvironmentError as e:
                        logger.error(e)
                        num_errors += 1

        logger.info("\nDeleted %d files and %d directories." % (num_files, num_dirs))
        if num_errors == 1:
            logger.info("There was 1 error")
        elif num_errors > 1:
            logger.info("There were %d errors." % num_errors)
        logger.info("*** Finished ***")
