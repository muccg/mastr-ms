# This code was copied out of django-test-extras and modified to work
# with Django 1.5. Hopefully soon we can just get it from PyPi.

from django.core import management
from django.core.management.commands import flush

class SkipFlushCommand(flush.Command):
    def handle_noargs(self, **options):
        return

    def __enter__(self):
        # hold onto the original and replace flush command with a no-op
        self.original_flush_command = management._commands['flush']
        management._commands['flush'] = self

    def __exit__(self, exc_type, exc_value, traceback):
        # unpatch flush back to the original
        management._commands['flush'] = self.original_flush_command

class NonFlushingTransactionTestCaseMixin(object):
    """
    Mixin that prevents the database from being flushed in TransactionTestCase
     subclasses.

    Only suitable for tests that don't change any database data - if your test
    does change the database then use DataPreservingTransactionTestCaseMixin
    instead.

    Only works if you mix it in first like this:
       class MyTestCase(NonFlushingTransactionTestCaseMixin, TransactionTestCase):
    not like this:
       class MyTestCase(TransactionTestCase, NonFlushingTransactionTestCaseMixin):

    Source:
    https://github.com/brightinteractive/django-test-extras/blob/master/test_extras/testcases.py
    """
    def _fixture_setup(self):
        """
        Overrides TransactionTestCase._fixture_setup() and replaces the flush
        command with a dummy command whilst it is running to prevent it from
        flushing the database.
        """
        with SkipFlushCommand():
            super(NonFlushingTransactionTestCaseMixin, self)._fixture_setup()

    def _fixture_teardown(self):
        with SkipFlushCommand():
            super(NonFlushingTransactionTestCaseMixin, self)._fixture_teardown()
