import time
import threading
import signal

class BaseCamera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    lastAccess = 0  # time of last client access to the camera
    killCamera = False

    def __init__(self):
        if BaseCamera.thread is None:
            # start background frame thread
            BaseCamera.thread = threading.Thread(target=self._thread)
            signal.signal(signal.SIGINT, self.handler)
            BaseCamera.thread.start()


    def handler(self):
        if BaseCamera.thread is not None:
            BaseCamera.killCamera = True

    @staticmethod
    def frames():
        """Generator that returns frames from the camera."""
        raise NotImplementedError('Must be implemented by subclasses.')

    def getFrame(self):
        """Return the current camera frame."""
        BaseCamera.lastAccess = time.time()
        return BaseCamera.frame

    @classmethod
    def _thread(cls):
        """Camera background thread."""
        print('Starting camera thread.')
        framesIterator = cls.frames()
        for frame in framesIterator:
            BaseCamera.frame = frame
            time.sleep(0.1)
            # if there hasn't been any clients asking for frames in
            # the last 10 seconds then stop the thread
            if time.time() - BaseCamera.lastAccess > 10:
                framesIterator.close()
                print('Stopping camera thread due to inactivity.')
                break
        BaseCamera.thread = None