import time
import logging
try:
    from pypylon import pylon
except:
    pylon = None

from . input import Input

log = logging.getLogger(__name__)

# writes the framenumber to the 8-11 bytes of the image as a big-endian set of octets
def encode_framenumber(np_image, n):
    for i in range(4):
        np_image[0][i+7] = n & 0xFF
        n>>=8

# converts time from a float in seconds to an int64 in microseconds
# writes the time to the first 7 bytes of the image as a big-endian set of octets
def encode_timestamp(np_image, timestamp):
    t = int(timestamp*1e6)
    for i in range(7):
        np_image[0][i] = t & 0xFF
        t>>=8

class CameraPylon(Input):
    '''
    Camera that interfaces with pylon/basler cameras.

    Args:
        id (int): Id of the pylon camera.
        config (dict): Configuration dictionary. Accepted keywords:
            pfs (str): path to a pfs file.
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'pfs': None,
            'channels': 1,
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)
        self.read_count = 0

    def configure(self):
        '''
        Pylon camera configuration. Requires the pylon camera to have been opened already.
        The order of these statements is important.
        Populates self.config with set values.
        Logs camera start.
        '''

        if self.config.get('pfs', None):
            pylon.FeaturePersistence.Load(self.config.get('pfs'), self.input.GetNodeMap())
        self.config['pixel_format'] = self.input.PixelFormat.Value
        self.config['gain'] = self.input.Gain.Value
        self.config['exposure_time'] = self.input.ExposureTime.Value
        self.config['res'] = (self.input.Width.Value, self.input.Height.Value)
        self.config['width'] = self.input.Width.Value
        self.config['height'] = self.input.Height.Value
        self.config['fps'] = self.input.ResultingFrameRate.GetValue()

    def open(self):
        self.read_count = 0
        # quick tips & tricks:
        # do not register the pylon camera with a software trigger - Mr. Brown
        # use OneByOne over LatestImageOnly to prevent frame loss - Mr. Brown
        try:
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            self.input = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[self.id]))
            self.input.Open()
            self.configure()

            self.input.StopGrabbing()
            self.input.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        except Exception as e:
            log.error(f'{str(self)} open error: {e}')

    def read(self):
        frame = None
        now = None
        if self.input:
            try:
                ret = self.input.RetrieveResult(100, pylon.TimeoutHandling_ThrowException)
                if ret.IsValid():
                    frame = ret.GetArray()
                now = time.time()
                encode_timestamp(frame,now)
                encode_framenumber(frame,self.read_count)
                self.read_count+=1
            except TypeError as e:
                log.error(f"{str(self)} read error: {e}")
            ret.Release()
        if now is None: now = time.time()
        return frame, now

    def close(self):
        self.read_count = 0
        if self.input and self.input.IsOpen():
            self.input.Close()
            self.input = None

if pylon is None:
    class PylonCamera(Input):
        def __init__(self, *args, **kargs):
            Input.__init__(self)
            log.error("PyPylon not found")