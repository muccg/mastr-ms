# -*- coding: utf-8 -*-

# Trying out selenium tests

#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver
from splinter import Browser
import re
from django.test.client import Client
from django.conf import settings

# dependencies
# yum -y install firefox
# pip install splinter selenium WebDriver

def create_session_store():
    """ Creates a session storage object. """

    from django.utils.importlib import import_module
    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore()
    store.save()
    return store

class AdminTests(LiveServerTestCase, XDisplayTest, WithFixtures):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpClass(cls):
        cls.setup_display()
        super(AdminTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.teardown_display()
        super(AdminTests, cls).tearDownClass()

    def test1_login(self):
        """
        Login to the admin page. This test is given as an example in
        the django docs.
        """
        self.setup_more_fixtures()
        self.selenium = WebDriver()
        self.selenium.get(self.url("/repoadmin/login/"))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.admin.username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.admin_password)
        self.selenium.find_element_by_xpath("//input[@value='Log in']").click()
        self.selenium.quit()

    def junk_code(self):
        session_store = create_session_store()
        session_items = session_store
        # Add a session key/value pair.
        session_items['uid'] = 1
        session_items.save()

        #test user setup
        email = "testuser"
        self.assertTrue(User.objects.filter(email=email).exists(),
                        "Test user exists")
        #success = self.client.login(email=email, password=password)
        #self.assertTrue(success, "Log in as test user")

            #logger.info("adding cookie %s=%s" % (settings.SESSION_COOKIE_NAME, session_store.session_key))
            #browser.cookies.add({settings.SESSION_COOKIE_NAME:
            #                     session_store.session_key})
            # logger.info("adding cookies %s" % str(self.client.cookies))
            # browser.cookies.add(dict((k, m.value) for (k, m) in self.client.cookies.items()))
            # self.assertEqual(unicode(browser.cookies[settings.SESSION_COOKIE_NAME]),
            #                  unicode(self.client.cookies[settings.SESSION_COOKIE_NAME].value))


    def test2_mark_incomplete(self):
        """
        Tests the admin action where a run can be set as incomplete.
        """

        # run setup
        self.setup_more_fixtures()
        self.assertEqual(Run.objects.count(), 1)

        # make the run complete
        self.run.runsample_set.update(complete=True)
        self.run.update_sample_counts()
        self.assertEqual(self.run.state, RUN_STATES.COMPLETE[0])

        with Browser() as browser:
            # select the run
            browser.visit(self.url("/repoadmin/repository/run/"))

            # fill out login form
            if browser.is_element_present_by_xpath("//input[@value='Log in']"):
                browser.fill("username", self.admin.email)
                browser.fill("password", self.admin_password)
                browser.find_by_xpath("//input[@value='Log in']").click()

            browser.find_by_name("_selected_action").first.check()

            # Select the "Mark Run Incomplete" action from dropdown box
            browser.select("action", "mark_run_incomplete")

            # Click "Go" button
            button = browser.find_by_name("index")
            button.click()

            self.assertTrue(browser.is_text_present("changed to incomplete"),
                            "Check for a status message")

            # grab status message
            message = browser.find_by_css(".messagelist").text
            logger.debug("message is: %s" % message)

            # check the number of samples and runs
            pat = re.compile(r"(\d+) runs? and (\d+) samples? changed to incomplete")
            m = pat.match(message)
            self.assertEqual(int(m.group(1)), 1, "Check num. runs changed")
            self.assertEqual(int(m.group(2)), 2, "Check num. samples changed")

    def url(self, path):
        return "%s%s" % (self.live_server_url, path)
