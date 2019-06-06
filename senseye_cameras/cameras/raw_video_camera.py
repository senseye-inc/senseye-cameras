import logging
import numpy as np

from senseye_utils.date_utils import timestamp_now

from . camera import Camera

log = logging.getLogger(__name__)


class RawVideoCamera(Camera):
    '''
    Treats raw video as a camera.

    Args:
        id (str): path to the raw video file.
        config (dict): Configuration dictionary. Accepted keywords:
            res (tuple): frame size
    '''

    def __init__(self, id=0, config={}):
        Camera.__init__(self, id=id, config=config)
        self.camera = None
        self.res = config.get('res', None)

    def open(self):
        '''
        Opens raw video as a bytes file.
        '''
        self.camera = open(self.id, 'rb')
        self.log_camera_start()

    def read(self):
        '''
        Reads in raw video.
        config['res'] dictates how many bytes are read in.
        '''
        frame = None

        # Length of frame in bytes
        frame_length = np.uint8().itemsize * np.product(self.res)
        bytes = self.camera.read(frame_length)

        buf = np.frombuffer(bytes, dtype=np.uint8)
        if buf.size != 0:
            frame = buf.reshape(self.res)
        return frame, timestamp_now()

    def close(self):
        if self.camera:
            self.camera.close()
