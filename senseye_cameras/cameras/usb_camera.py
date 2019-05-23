import cv2
import logging

from senseye_utils.date_utils import timestamp_now

from . camera import Camera

log = logging.getLogger(__name__)


class UsbCamera(Camera):
    '''
    Opens a usb camera or video using OpenCV.
    '''

    def __init__(self, id=0, config={}):
        Camera.__init__(self, id=id, config=config)

        self.camera = None
        self.format = config.get('FORMAT', 'MJPG')

        self.defaults = {
            'fps': 30,
            'codec': 'MJPG',
        }

    def configure(self, config={}, defaults={}):
        '''
        Configures the camera using a config.
        Supported configurations: fps, codec, res
        '''
        c = {**defaults, **config}
        log.debug(f"Configuring camera {self.id}: {c}")

        if 'fps' in c:
            self.camera.set(cv2.CAP_PROP_FPS, c['fps'])
        if 'codec' in c:
            self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*c['codec']))
        if 'res' in c:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, c['res'][0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, c['res'][1])

    def open(self):
        self.camera = cv2.VideoCapture(self.id)

        if not self.camera.isOpened():
            log.warning(f'Video {self.id} failed to open. Video is corrupt, or an unreadable format.')
        else:
            self.configure(config=self.config, defaults=self.defaults)


    def read(self):
        '''
        Reads in frames.
        Converts frames from BGR to the more commonly used RGB format.
        '''
        if self.camera is None:
            return None, timestamp_now()

        ret, frame = self.camera.read()

        if not ret or frame is None:
            return None, timestamp_now()

        # bgr to rgb
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame, timestamp_now()

    def close(self):
        if self.camera:
            self.camera.release()
            self.camera = None
