import sys
import os.path
import threading
import signal
import time
import logging
import wx
import mastrms.mdatasync_client.client
# client has some libs in subdirectories
sys.path.append(os.path.dirname(mastrms.mdatasync_client.client.__file__))
from mastrms.mdatasync_client.client.main import MDataSyncApp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

__all__ = ["TestClient"]

# fixme: unit tests don't show exceptions in other threads

class TestClient(object):
    """
    This class runs the client in a thread and provides methods for
    unit tests to control the client.

    The test client uses wxWidgets and so needs an X display.
    ``Xephyr`` or ``Xvfb`` can be used for this purpose.

    The `config` parameter should be a
    :class:`mastrms.mdatasync_client.client.config.MSDSConfig` object.

    If `maximize` is True, then the main window will be maximized,
    which is helpful when watching tests run in a nested X server.
    """
    clients = []

    # give the test case 60 seconds to run
    MAX_TIME = 60

    def __init__(self, config, maximize=False):
        logger.info("TestClient starting")
        logger.info("Config\n%s" % config)
        self.config = config
        self.maximize = maximize
        self.lock = threading.RLock()
        self.ready = threading.Event()
        self.finished = threading.Event()
        self.have_quit = False
        self.thread = threading.Thread(target=self._client_thread)
        self.thread.start()
        self._wait_for_ready()
        logger.debug("TestClient ready")
        self.__class__.clients.append(self)

    def _client_thread(self):
        logger.info("TestClient mainloop thread")
        self.m = MDataSyncApp(self.config)
        if self.maximize:
            self.m.win.Maximize()
        logger.addHandler(self.m.win.getLog())
        self._setup_exit_hook()
        self._post_start_event()
        self.m.MainLoop()
        logger.info("Mainloop finished")
        self.m.msds.stopThread()

    def _post_start_event(self):
        wx.CallAfter(self._set_ready, True)

    def _set_ready(self, ready=True):
        if ready:
            self.ready.set()
        else:
            self.ready.clear()

    def click_sync(self):
        """Clicks the "Check Now" menu item."""
        logger.info("click_sync enter")
        wx.CallAfter(self.m.win.OnCheckNow, None)
        logger.info("click_sync exit")
        self._wait_for_sync()

    def _wait_for_sync(self):
        CRAP_TEST_CRAP = 4
        logger.debug("sleeping for %ds" % CRAP_TEST_CRAP)
        time.sleep(CRAP_TEST_CRAP)

    def _wait(self):
        CRAP_TEST_CRAP = 1
        logger.debug("sleeping for %ds" % CRAP_TEST_CRAP)
        time.sleep(CRAP_TEST_CRAP)

    def click_send_log(self):
        """Clicks the "Send Log" button."""
        wx.CallAfter(self.m.win.OnSendLog)
        self._wait_for_sync()

    def click_send_shot(self):
        """Clicks the "Send Shot" screenshot button."""
        wx.CallAfter(self.m.win.OnTakeScreenshot)
        self._wait_for_sync()

    class TestPreferences(object):
        def __init__(self, prefs):
            self.win = prefs
            self.advanced = None

        def _wait(self):
            time.sleep(2)

        def click_refresh(self):
            self.win.fixme
            self._wait()

        def click_send_key(self):
            wx.CallAfter(self.win.OnSendKey, None)
            self._wait()

        def click_send_handshake(self):
            wx.CallAfter(self.win.OnHandshake, None)
            self._wait()

        def close(self):
            wx.CallAfter(self.win.OKPressed)
            self._wait()

        def click_advanced(self):
            wx.CallAfter(self.win.openAdvancedPrefs, None)
            self._wait()
            self.advanced = self.win.advanced
            return self

        def advanced_click_close(self):
            assert self.advanced is not None
            wx.CallAfter(self.advanced.OKPressed)
            self._wait()
            self.advanced = None # assume window was closed

    def click_menu_preferences(self):
        """
        Clicks the *Edit -> Preferences* menu. This method returns a
        `TestPreferences` object which can be used to control the
        preferences window.
        """
        wx.CallAfter(self.m.win.OnMenuPreferences, None)
        self._wait()
        return self.TestPreferences(self.m.win.prefs)

    def _wait_for_ready(self):
        self.ready.wait()

    def set_window_title(self, title):
        """Changes the main window title, useful for showing the test
        case name."""
        wx.CallAfter(self.m.win.SetTitle, title)

    def close(self):
        """
        Closes window, but doesn't quit (app is minimized to tray).
        """
        wx.CallAfter(self.m.win.Close)
        self._wait()

    def minimize(self):
        """
        Closes window, but doesn't quit (app is minimized to tray).
        """
        wx.CallAfter(self.m.win.OnMenuMinimise, None)
        self._wait()

    def activate_tray_icon(self):
        "Same as double-clicking tray icon"
        wx.CallAfter(self.m.win.SystrayIcon.OnTaskBarActivate, None)
        self._wait()

    def quit(self, force=False):
        """
        Cleanly quits the client, unless it is already in the process
        of quitting, or if the ``TEST_CLIENT_LINGER`` environment
        variable is non-zero. The ``TEST_CLIENT_LINGER`` environment
        variable is overridden by the `force` argument to this method.
        """
        if not force and self._should_linger():
            logger.info("Not quitting client due to TEST_CLIENT_LINGER setting")
        elif not self.have_quit:
            logger.info("Quitting")
            wx.CallAfter(self.m.win.OnMenuQuit, None)
            self.thread.join()
            self.have_quit = True

    def _should_linger(self):
        """
        For debugging test cases, it is sometimes handy to keep the
        client open. This can be controlled with an environment
        variable.
        """
        linger = os.environ.get("TEST_CLIENT_LINGER", "")
        try:
            return int(linger) != 0
        except ValueError:
            return bool(linger)

    def _setup_exit_hook(self):
        def set_finished(event):
            logger.debug("Window closed")
            self.finished.set()
        wx.EVT_CLOSE(self.m.win, set_finished)

    def __del__(self):
        self.__class__.clients.remove(self)
        super(TestClient, self).__del__()

    @classmethod
    def kill_all(cls):
        for client in cls.clients:
            client.quit()
