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
            'binning': 0,
            'decimation': 1,
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)
        self.writing = False
        self.path = path

    def configure(self):

        self.config['gain'] = self.set_prop('Gain', self.config['gain'])

        width = self.set_prop('Width', self.config['res'][0])
        height = self.set_prop('Height', self.config['res'][1])

        # set binning and decimation to make output files smaller
        self.input.set_binning(self.config['binning']);
        self.input.set_decimation(self.config['decimation']);

        self.config['res'] = (width//self.input.get_scaling(), height//self.input.get_scaling())

        # exposure must be minimized before setting frame rate
        self.set_prop('Exposure', 'min')
        self.config['fps'] = self.set_prop('FrameRate', self.config['fps'])
        self.config['exposure'] = self.set_prop('Exposure', self.config['exposure'])

        # # center AOI on sensor
        self.config['offset_x'] = self.set_prop('OffsetX', self.get_prop('OffsetX', flag='max')//2)
        self.config['offset_y'] = self.set_prop('OffsetY', self.get_prop('OffsetX', flag='min')//2)

    def start_reading(self):
        try:
            self.input.start_reading()
        except Exception as e:
            log.error(f'Failed to start reading with error {e}')

    def stop_reading(self):
        try:
            self.input.stop_reading()
        except Exception as e:
            log.error(f'Failed to stop reading with error {e}')

    def get_prop(self, name, flag=None):
        if flag is None:
            return self.input.get_uint_param(name)
        if flag == 'min':
            return self.input.get_uint_param_min(name)
        if flag == 'max':
            return self.input.get_uint_param_max(name)
        log.error(f'get_prop flag {flag} not supported.')

    def set_prop(self, name, value):
        ret = None
        if value == 'max' or value == 'min':
            value = self.get_prop(name, flag=value)

        if type(value) is int:
            ret = self.input.set_uint_param(name, value)
        elif type(value) is str:
            ret = self.input.set_enum_param(name, value)
        else:
            log.error(f'Invalid Type. Cannot set type {type(value)}')

        if ret != value:
            log.warning(f'Failed to set {name} to {value}. {name} set to {ret} instead.')
        return ret

    def open(self):
        self.input = pyemergent.PyEmergent()
        open_error = self.input.open()
        if open_error != 0:
            self.input.stop_reading()
            log.error(f'{str(self)} open error: {open_error}')
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
        timestamp = None

        try:
            frame_bytes, timestamp = self.input.read()
            buf = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = buf.reshape(self.config.get('res')[::-1])
        except Exception as e:
            log.error(f'{str(self)} read error: {e}')

        return frame, timestamp

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
