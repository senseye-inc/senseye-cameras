import logging

from senseye_utils import LoopThread
from senseye_utils.rapid_events import RapidEvents

from . cameras.camera_factory import create_camera

log = logging.getLogger(__name__)


class CameraReader(LoopThread):
    '''
    Reads in frames and emits them using RapidEvents ZMQ
    Creates a camera instance given camera_type, camera_config, and camera_id.

    Args:
        camera_feed (string): name of the RapidEvents event published every time a frame is read.
    '''

    def __init__(self, camera_feed=None, camera_type='usb', camera_config={}, camera_id=0):
        LoopThread.__init__(self, frequency=100)

        self.camera = create_camera(camera_type=camera_type, config=camera_config, id=camera_id)
        self.camera_type = camera_type
        self.camera_id = camera_id

        self.re = None
        self.camera_feed = camera_feed
        if self.camera_feed is None:
            self.camera_feed = f'camera_reader:publish:{camera_type}:{camera_id}'

    def on_start(self):
        '''
        Opens the camera and initializes RapidEvents.
        '''
        self.camera.open()
        self.re = RapidEvents(f'camera_reader:{self.camera_type}:{self.camera_id}')
        log.info(f"Creating camera_reader tied to {self.camera_type}:{self.camera_id}. Publishing to {self.camera_feed}")


    def loop(self):
        '''
        Reads in frames.
        '''
        frame, timestamp = self.camera.read()
        if frame is not None:
            self.re.publish(self.camera_feed, frame=frame, timestamp=timestamp)

    def on_stop(self):
        '''
        Cleans up our camera and RapidEvents instances.
        '''
        if self.camera:
            self.camera.close()
            self.camera = None

        if self.re:
            self.re.stop()
            self.re = None

        log.info(f'Camera {self.camera_type}:{self.camera_id} closing.')
