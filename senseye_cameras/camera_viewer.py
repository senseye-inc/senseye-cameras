import cv2
import logging

from senseye_utils import LoopThread
from senseye_utils.rapid_events import RapidEvents

log = logging.getLogger(__name__)


class CameraViewer(LoopThread):
    def __init__(self, camera_feed=None, camera_config={}, scale=0.5):
        LoopThread.__init__(self, frequency=100)

        self.camera_feed = camera_feed
        self.camera_config = camera_config
        self.scale = scale
        self.frame = None


        self.re = RapidEvents(f'camera_viewer:{self.camera_feed}')
        self.re.connect(self.on_frame_read, self.camera_feed)

        log.info(f"Creating camera_viewer. Listening to {self.camera_feed}")

    def on_frame_read(self, frame=None):
        '''
        Function triggered upon camera_feed.
        Cannot cv.imshow on this function (gui functions can't be run on a separate thread)
        '''
        # convert frame
        if self.camera_config.get('pixel_format', None) == 'BayerRG8':
            frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_GR2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # resize frame
        self.frame = cv2.resize(frame, (int(frame.shape[1] * self.scale), int(frame.shape[0] * self.scale)))


    def loop(self):
        if self.frame is not None:
            cv2.imshow(f'camera_viewer:{self.camera_feed}', self.frame)
            cv2.waitKey(1)

    def on_stop(self):
        cv2.destroyAllWindows()
        if self.re:
            self.re.stop()
            self.re = None
