import logging
try:
    import pyemergent
except:
    pyemergent = None
import numpy as np

from senseye_utils.date_utils import timestamp_now

from . input import Input

log = logging.getLogger(__name__)


class CameraEmergent(Input):
    '''
    Reads in frames from pyemergent.
    Args:
        id (str): path to the raw video file.
        config (dict): Configuration dictionary. Accepted keywords:
            res (tuple): frame size
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'res': (1920, 1080),
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

    def open(self):
        '''Opens raw video as a bytes file.'''
        self.input = pyemergent.PyEmergent()
        self.input.open()
        self.log_start()

    def read(self):
        '''
        Reads in raw video.
        config['res'] dictates how many bytes are read in.
        '''
        frame = None

        try:
            frame_bytes = self.input.read()
            buf = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = buf.reshape(self.config.get('res'))
        except: pass

        return frame, timestamp_now()

    def close(self):
        if self.input:
            self.input.close()
        self.input = None

if pyemergent is None:
    class CameraEmergent(Input):
        def __init__(self, *args, **kargs):
            Input.__init__(self)
            log.error("pyemergent not found")
