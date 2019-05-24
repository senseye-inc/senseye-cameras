import logging
try:
    from pypylon import pylon
except Exception:
    pylon = None

from senseye_utils.date_utils import timestamp_now

from . camera import Camera

log = logging.getLogger(__name__)


class PylonCamera(Camera):
    def __init__(self, id=0, config={}):
        Camera.__init__(self, id=id, config=config)

        # set up config
        self.defaults = {
            'fps': 60,
            'color': True,
            'pixel_format': 'BayerRG8',
            'exposure_time': 1000000//60 - 500,
            'res': (1800, 1800)
        }
        self.config = {**self.defaults, **self.config}

    def configure(self):
        '''
        Pylon camera configuration. Requires the pylon camera to have been opened already.
        The order of these statements is important.
        Populates self.config with set values.
        Logs camera start.
        '''
        if self.config.get('color', False):
            try:
                self.camera.PixelFormat.SetValue(self.config.get('pixel_format'))
            except Exception:
                log.info(f'Pixel Format not set to {self.config.get("pixel_format")}, set to {self.camera.PixelFormat} instead.')
        self.camera.CenterX.Value = False
        self.camera.CenterY.Value = False
        self.maxW = self.camera.Width.Max
        self.maxH = self.camera.Height.Max
        self.camera.ReverseX.Value = True
        self.camera.ReverseY.Value = False
        self.camera.Gain.Value = 12
        self.camera.ExposureTime.SetValue(self.config.get('exposure_time'))

        self.camera.AcquisitionFrameRateEnable.Value = True
        self.camera.OffsetX.Value = 0
        self.camera.CenterX.Value = True
        self.camera.OffsetY.Value = 0
        self.camera.CenterY.Value = False
        self.camera.Width.Value = self.config.get('res')[0]
        self.camera.Height.Value = self.config.get('res')[1]
        self.camera.AcquisitionFrameRate.SetValue(self.config.get('fps'))

        self.config['pixel_format'] = self.camera.PixelFormat
        self.config['gain'] = self.camera.Gain.Value
        self.config['exposure_time'] = self.camera.ExposureTime.Value
        self.config['res'] = (self.camera.Width.Value, self.camera.Height.Value)
        self.config['fps'] = self.camera.AcquisitionFrameRate.Value
        self.log_camera_start()

    def open(self):
        # quick tips & tricks:
        # do not register the pylon camera with a software trigger - Mr. Brown
        # use OneByOne over LatestImageOnly to prevent frame loss - Mr. Brown
        try:
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[self.id]))
            self.camera.Open()
            self.configure()

            self.camera.StopGrabbing()
            self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
        except Exception as e:
            log.error(f"Pylon camera open failed: {e}")

    def read(self):
        frame = None

        ret = self.camera.RetrieveResult(100, pylon.TimeoutHandling_ThrowException)
        try:
            if ret.IsValid():
                frame = ret.GetArray()
        except TypeError as e:
            log.error(f'PylonCamera read error: {e}')
        ret.Release()

        return frame, timestamp_now()

    def close(self):
        if self.camera.IsOpen():
            self.camera.Close()
            self.camera = None

# Fallback for no pylon
if pylon is None:
    class PylonCamera(Camera):
        def __init__(self, *args, **kargs):
            Camera.__init__(self)
            log.error("PyPylon not found")
