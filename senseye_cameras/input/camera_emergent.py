import logging
import numpy as np
try:
    import pyemergent
except:
    pyemergent = None

from senseye_utils.date_utils import timestamp_now
from senseye_utils import Events

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

    def __init__(self, id=0, config={}, path=None):
        defaults = {
            'res': (1920, 1080),
            'gain': 1024,
            'fps': 100,
            'exposure': 2400,
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)
        self.writing = False
        self.path = path

    def configure(self):
        width = self.input.set_param('Width', self.config['res'][0])
        height = self.input.set_param('Height', self.config['res'][1])
        self.config['emergent_res'] = (width, height)
        self.config['emergent_gain'] = self.input.set_param('Gain', self.config['gain'])
        self.config['emergent_fps'] = self.input.set_param('FrameRate', self.config['fps'])
        self.config['emergent_exposure'] = self.input.set_param('Exposure', self.config['exposure'])

    def configure(self):
        width = self.input.set_param('Width', self.config['res'][0])
        height = self.input.set_param('Height', self.config['res'][1])
        self.config['emergent_res'] = (width, height)
        self.config['emergent_gain'] = self.input.set_param('Gain', self.config['gain'])
        self.config['emergent_fps'] = self.input.set_param('FrameRate', self.config['fps'])
        self.config['emergent_exposure'] = self.input.set_param('Exposure', self.config['exposure'])

    def set_path(self, path):
        self.path = path
        if self.input:
            self.input.set_path(self.path)

    def start_writing(self):
        self.writing = True
        if self.input:
            self.input.start_writing()

    def open(self):
        self.input = pyemergent.PyEmergent(config=self.config)
        open_error = self.input.open()
        if open_error != 0:
            log.error(f'{str(self)} open error: {open_error}')
        if self.writing:
            self.input.start_writing()
        if self.path:
            self.input.set_path(self.path)
        self.configure()
        self.input.start()

    def read(self):
        '''
        Reads in raw video.
        config['res'] dictates how many bytes are read in.
        '''
        frame = None

        try:
            frame_bytes = self.input.read()
            buf = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = buf.reshape(self.config.get('res')[::-1])
        except Exception as e:
            log.error(f'{str(self)} read error: {e}')

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
