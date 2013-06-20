import unittest
from mastrms.mdatasync_client.client.MSDataSyncAPI import DataSyncServer
from mastrms.mdatasync_client.client.config import MSDSConfig
import dingus

from mastrms.mdatasync_client.client.test.testclient import *

class BasicClientTests(unittest.TestCase):
    def setUp(self):
        config = MSDSConfig()
        self.client = TestClient(config)

    def tearDown(self):
        self.client.quit()

    def test1_mainwindow(self):
        self.assertTrue(self.client.m.win.IsShownOnScreen(),
                        "Window is on screen")

    def test2_tray_minimize_maximize(self):
        self.client.close() # doesn't seem to disappear window
        #self.assertFalse(self.client.m.win.IsShownOnScreen(),
        #                 "Window exists but is hidden")
        self.client.minimize()
        self.assertFalse(self.client.m.win.IsShownOnScreen(),
                         "Window exists but is hidden")
        self.client.activate_tray_icon()
        self.assertTrue(self.client.m.win.IsShownOnScreen(),
                        "Window is on screen again")

    def test3_preferences_window(self):
        "Exercise the code which shows preferences dialog"
        prefs = self.client.click_menu_preferences()
        prefs.close()

    def test3_advanced_preferences_window(self):
        "Exercise advanced preferences dialog code"
        prefs = self.client.click_menu_preferences()
        advanced = prefs.click_advanced()
        advanced.advanced_click_close()
        prefs.close()

class DataSyncServerTests(unittest.TestCase):
    def setUp(self):
        config = MSDSConfig(user="user",
                            sitename=self.nc.site_name,
                            stationname=self.nc.station_name,
                            organisation=self.nc.organisation_name,
                            localdir=unicode(self.simulator.destdir),
                            synchub="%s/sync/" % self.live_server_url,
                            logfile=logfile.name,
                            loglevel=plogging.LoggingLevels.DEBUG,
                            archivesynced=False,
                            archivedfilesdir=archivedir)

        self.server = DataSyncServer(config)
