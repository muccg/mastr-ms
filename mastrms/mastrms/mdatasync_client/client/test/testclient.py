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

# fixme: unit tests don't show exceptions in other threads
# fixme: this requires DISPLAY pointing to an X server, e.g. Xephyr

class TestClient(object):
    """
    This class runs the client in a thread and provides methods for
    unit tests to control the client.
    """
    clients = []

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
        logger.info("click_sync enter")
        wx.CallAfter(self.m.win.OnCheckNow, None)
        logger.info("click_sync exit")
        self._wait_for_sync()

    def _wait_for_sync(self):
        CRAP_TEST_CRAP = 4
        logger.debug("sleeping for %ds" % CRAP_TEST_CRAP)
        time.sleep(CRAP_TEST_CRAP)

    def _wait_for_ready(self):
        self.ready.wait()

    def set_window_title(self, title):
        wx.CallAfter(self.m.win.SetTitle, title)

    def quit(self, force=False):
        """
        Cleanly quits the client, unless it is already in the process
        of quitting, or if the TEST_CLIENT_LINGER environment variable
        is non-zero. The TEST_CLIENT_LINGER environment variable is
        overridden by the `force' argument to this method.
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

def ctrlc_handler(signame, frame):
    TestClient.kill_all()

signal.signal(signal.SIGINT, ctrlc_handler)
