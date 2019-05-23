import logging
import numpy as np

from senseye_utils.date_utils import timestamp_now

from . camera import Camera

log = logging.getLogger(__name__)


class RawVideoCamera(Camera):
    '''
    Treats raw video as a camera.
    '''

    def __init__(self, id=0, config={}):
        Camera.__init__(self, id=id, config=config)
        self.camera = None

    def open(self):
        '''
        Opens raw video as a bytes file.
        '''
        self.camera = open(self.id, 'rb')

    def read(self):
        '''
        Reads in raw video.
        config['res'] dictates how many bytes are read in.
        '''
        frame = None

        # Length of frame in bytes
        frame_length = np.uint8().itemsize * np.product(self.res)
        frame = self.camera.read(frame_length)

        if frame is not None:
            return np.frombuffer(frame, dtype=np.uint8).reshape(self.res), timestamp_now()

    def close(self):
        if self.camera:
            self.camera.close()
