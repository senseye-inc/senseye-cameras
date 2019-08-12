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
        width = self.set_prop('Width', self.config['res'][0])
        height = self.set_prop('Height', self.config['res'][1])
        self.input.set_res(width * height)
        self.config['res'] = (width, height)
        self.set_prop('Exposure', self.get_prop('Exposure')['min']) # allows any fps to be set
        self.config['fps'] = self.set_prop('FrameRate', self.config['fps'])
        if self.config['exposure'] == 'max':
            max = self.get_prop('Exposure')['max']
            self.config['exposure'] = self.set_prop('Exposure', max)
        else:
            self.config['exposure'] = self.set_prop('Exposure', self.config['exposure'])
        self.config['gain'] = self.set_prop('Gain', self.config['gain'])
        self.config['max_width'] = self.get_prop('Width')['max']
        self.config['max_height'] = self.get_prop('Height')['max']
        self.config['max_offset_x'] = self.get_prop('OffsetX')['max']
        self.config['max_offset_y'] = self.get_prop('OffsetY')['max']
        # center AOI on sensor
        self.config['offset_x'] = self.set_prop('OffsetX', self.config['max_offset_x']//2)
        self.config['offset_y'] = self.set_prop('OffsetY', self.config['max_offset_y']//2)
        self.config['focus'] = self.set_prop('Focus', 0)

    def set_path(self, path):
        self.path = path
        if self.input:
            self.input.set_path(self.path)

    def start_writing(self):
        self.writing = True
        if self.input:
            self.input.start_writing()

    def stop_writing(self):
        self.writing = False
        if self.input:
            self.input.stop_writing()

    def start_reading(self):
        if self.input:
            self.input.start_reading()

    def stop_reading(self):
        if self.input:
            self.input.stop_reading()

    def get_prop(self, name):
        return {
            'cur': self.input.get_uint_param(name),
            'min': self.input.get_uint_param_min(name),
            'max': self.input.get_uint_param_max(name),
        }

    def set_prop(self, name, value):
        if type(value) is int:
            return self.input.set_uint_param(name, value)
        if type(value) is str:
            return self.input.set_enum_param(name, value)
        return f'Invalid Type. Cannot set type {type(value)}'

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
            self.input.stop_reading()
            self.input.close()
        self.input = None

if pyemergent is None:
    class CameraEmergent(Input):
        def __init__(self, *args, **kargs):
            Input.__init__(self)
            log.error("pyemergent not found")
