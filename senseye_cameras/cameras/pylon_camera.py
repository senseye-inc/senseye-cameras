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

        devices = pylon.TlFactory.GetInstance().EnumerateDevices()
        if len(devices) == 0:
            raise pylon.RUNTIME_EXCEPTION("No cameras present.")

        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(devices[id]))
        # DO NOT REGISTER THE CAMERA WITH A SOFTWARE TRIGGER. JUST LET IT INIT WITH DEFAULTS

        # TODO Config options for color
        self.camera.Open()

        # COLOR BASLER
        if config['COLOR']:
            try:
                self.camera.PixelFormat.SetValue('BayerRG8')
            except Exception:
                log.info(
                    'Pixel Format failed to set to BayerRG8.'
                    f' Set to: {self.camera.PixelFormat} instead'
                )

        self.camera.CenterX.Value = False
        self.camera.CenterY.Value = False
        self.maxW = self.camera.Width.Max
        self.maxH = self.camera.Height.Max
        self.camera.ReverseX.Value = True
        self.camera.ReverseY.Value = False
        self.camera.Gain.Value = 12
        self.camera.ExposureTime.SetValue(config['EXPOSURE_TIME'])

        self.camera.AcquisitionFrameRateEnable.Value = True
        self.camera.OffsetX.Value = 0
        self.camera.CenterX.Value = True
        self.camera.OffsetY.Value = 0
        self.camera.CenterY.Value = False
        self.camera.Width.Value = self.width
        self.camera.Height.Value = self.height
        self.camera.AcquisitionFrameRate.SetValue(self.fps)

        log.info(f'PylonCamera fps: {self.fps}, resolution: {self.camera.Width.Value}, {self.camera.Height.Value}')

    def open(self):
        # USE OneByOne over LatestImageOnly to prevent the Basler's
        # framebuffer from erasing over itself
        self.camera.StopGrabbing()
        self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

    def read(self):
        ret = self.camera.RetrieveResult(100, pylon.TimeoutHandling_ThrowException)

        if not ret.IsValid():
            log.error('Invalid frame')
            ret.Release()
            return None, None

        try:
            frame = ret.GetArray()
            timestamp = ret.GetTimeStamp() / 1000

            if self.time_offset is None:
                self.time_offset = timestamp_now() - timestamp

            timestamp += self.time_offset

            ret.Release()

            return frame, timestamp

        except TypeError as e:
            log.error(e)
            return None, None

    def close(self):
        if self.camera.IsOpen():
            self.camera.Close()


# Fallback for no pylon
if pylon is None:
    class PylonCamera(Camera):
        def __init__(self, *args, **kargs):
            Camera.__init__(self)
            log.error("PyPylon not found")
