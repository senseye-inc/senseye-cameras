import logging
try:
    from pypylon import pylon
except:
    pylon = None

from senseye_utils.date_utils import timestamp_now

from . input import Input

log = logging.getLogger(__name__)


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
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

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
        self.config['fps'] = self.input.ResultingFrameRate.GetValue()

    def open(self):
        # quick tips & tricks:
        # do not register the pylon camera with a software trigger - Mr. Brown
        # use OneByOne over LatestImageOnly to prevent frame loss - Mr. Brown
        try:
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            self.input = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[self.id]))
            self.input.Open()
            self.configure()

            self.input.StopGrabbing()
            self.input.StartGrabbing(pylon.GrabStrategy_OneByOne)
        except Exception as e:
            log.error(f'{str(self)} open error: {e}')

    def read(self):
        frame = None

        ret = self.input.RetrieveResult(100, pylon.TimeoutHandling_ThrowException)
        try:
            if ret.IsValid():
                frame = ret.GetArray()
        except TypeError as e:
            log.error(f"{str(self)} read error: {e}")
        ret.Release()

        return frame, timestamp_now()

    def close(self):
        if self.input.IsOpen():
            self.input.Close()
            self.input = None

if pylon is None:
    class PylonCamera(Input):
        def __init__(self, *args, **kargs):
            Input.__init__(self)
            log.error("PyPylon not found")
