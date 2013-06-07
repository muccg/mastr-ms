import threading
import sys
import os.path
import logging
import wx
import mastrms.mdatasync_client.client
# client has some libs in subdirectories
sys.path.append(os.path.dirname(mastrms.mdatasync_client.client.__file__))
from mastrms.mdatasync_client.client.main import MDataSyncApp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# fixme: unit tests don't show errors in other threads

class TestClient(object):
    """
    This class runs the client in a thread and provides methods for
    unit tests to control the client.
    """
    def __init__(self, config):
        logger.info("TestClient starting")
        logger.info("Config\n%s" % config)
        self.config = config
        self.lock = threading.RLock()
        self.ready = threading.Event()
        self.finished = threading.Event()
        self.thread = threading.Thread(target=self._client_thread)
        self.thread.start()
        self._wait_for_ready()
        logger.debug("TestClient ready")

    def _client_thread(self):
        logger.info("TestClient mainloop thread")
        self.m = MDataSyncApp(self.config)
        logger.addHandler(self.m.win.getLog())
        self._setup_exit_hook()
        self._post_start_event()
        self.m.MainLoop()
        logger.info("Mainloop finished")
        self.m.msds.stopThread()

    def _post_start_event_wrong(self):
        timer = wx.Timer(self.m.win, 42)
        def set_ready(event):
            logger.info("TestClient mainloop ready")
            self._set_ready(True)
            timer.Stop()
            timer.Destroy()
        wx.EVT_TIMER(self.m.win, timer.GetId(), set_ready)
        timer.Start(10, True) # 10ms

    def _post_start_event(self):
        wx.CallAfter(self._set_ready, True)

    def _set_ready(self, ready=True):
        # with self.lock:
        #     self.ready=ready

        if ready:
            self.ready.set()
        else:
            self.ready.clear()

    def click_sync(self):
        logger.info("click_sync enter")
        #self.m.win.OnCheckNow(None)
        wx.CallAfter(self.m.win.OnCheckNow, None)
        logger.info("click_sync exit")

    def _wait_for_ready(self):
        #with self.lock:
            #while not self.ready:
            #    self.lock.wait()
        self.ready.wait()

    def _wait_for_finished(self):
        #with self.lock:
            #while not self.finished:
            #    self.lock.wait()
        self.finished.wait()

    def quit(self):
        logger.info("Quitting")
        wx.CallAfter(self.m.win.OnMenuQuit, None)
        #self._wait_for_finished()
        self.thread.join()

    def _setup_exit_hook(self):
        # def set_finished(event):
        #     logger.debug("Window closed")
        #     #with self.lock:
        #         #self.finished = True
        #     self.finished.set()

        # wx.EVT_CLOSE(self.m.win, set_finished)
        pass
