import cv2
import logging

from senseye_utils.date_utils import timestamp_now

from . camera import Camera

log = logging.getLogger(__name__)


class UsbCamera(Camera):
    '''
    Opens a usb camera or video using OpenCV.

    Args:
        id (int OR str): id of the camera, or path to a video file.
        config (dict): Configuration dictionary. Accepted keywords:
            res (tuple): frame size
            codec (str)
            fps (int)
    '''

    def __init__(self, id=0, config={}):
        Camera.__init__(self, id=id, config=config)

        # set up config
        self.defaults = {
            'fps': 30,
            'codec': 'MJPG',
        }
        self.config = {**self.defaults, **self.config}

        self.camera = None

    def configure(self):
        '''
        Configures the camera using a config.
        Supported configurations: fps, codec, res

        Fills self.config with camera attributes.
        Logs camera start.
        '''
        if 'fps' in self.config:
            self.camera.set(cv2.CAP_PROP_FPS, self.config.get('fps'))
        if 'codec' in self.config:
            self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.config.get('codec')))
        if 'res' in self.config:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.get('res')[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.get('res')[1])

        self.config['res'] = (int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)), 3)
        self.config['fps'] = (int(self.camera.get(cv2.CAP_PROP_FPS)))
        self.config['codec'] = (int(self.camera.get(cv2.CAP_PROP_FOURCC)))

        self.log_camera_start()

    def open(self):
        self.camera = cv2.VideoCapture(self.id)

        if not self.camera.isOpened():
            log.warning(f'Video {self.id} failed to open. Video is corrupt, or an unreadable format.')
        else:
            self.configure()

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
