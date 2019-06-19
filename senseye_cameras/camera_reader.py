import logging

from senseye_utils import LoopThread, RapidEvents

from . input.input_factory import create_input

log = logging.getLogger(__name__)


class CameraReader(LoopThread):
    '''
    Reads in frames and emits them using RapidEvents ZMQ
    Creates a camera instance given camera_type, camera_config, and camera_id.

    Args:
        camera_feed (string): Name of the RapidEvents event published every time a frame is read.
        camera_type (str): See 'create_camera' documentation.
        camera_config (dict): Configures the camera.
        camera_id (str OR int)
    '''

    def __init__(self, camera_feed=None, camera_type='usb', camera_config={}, camera_id=0):
        LoopThread.__init__(self, frequency=-1)

        self.camera_id = camera_id
        self.camera_type = camera_type
        self.camera = create_input(type=camera_type, config=camera_config, id=camera_id)
        self.camera.open()

        self.re = RapidEvents(f'camera_reader:{str(self)}')
        self.camera_feed = camera_feed if camera_feed else f'camera_reader:publish:{camera_type}:{camera_id}'

    def on_start(self):
        log.info(f"Creating camera_reader tied to {str(self)}. Publishing to {self.camera_feed}")

    def loop(self):
        '''Reads in frames.'''
        frame, timestamp = self.camera.read()
        if frame is not None:
            self.re.publish(self.camera_feed, frame=frame, timestamp=timestamp)

    def on_stop(self):
        '''Cleans up our camera and RapidEvents instances.'''
        if self.camera:
            self.camera.close()
        self.camera = None

        if self.re:
            self.re.stop()
        self.re = None

        log.info(f'Camera {str(self)} closing.')

    def __str__(self):
        return f'{self.camera_type}:{self.camera_id}'
