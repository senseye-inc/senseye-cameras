import cv2
import numpy as np
import logging

from senseye_utils import LoopThread, RapidEvents

log = logging.getLogger(__name__)


class CameraViewer(LoopThread):
    '''
    Args:
        camera_feed (str): RapidEvent channel that this object listens to for frames
        camera_config (dict): Configuration dictionary. Accepted keywords:
            pixel_format (str)
        scale (int): How much to decimate displayed frames. Values greater than 1 will enlarge frames.

    '''
    def __init__(self, camera_feed=None, camera_config={}, scale=0.5, focus=True):
        LoopThread.__init__(self, frequency=100)

        self.camera_feed = camera_feed
        self.camera_config = camera_config
        self.scale = scale
        self.frame = None
        self.focus = focus

        self.re = RapidEvents(f'camera_viewer:{self.camera_feed}')
        self.re.connect(self.on_frame_read, self.camera_feed)

        log.info(f"Creating camera_viewer. Listening to {self.camera_feed}")

    def on_frame_read(self, frame=None):
        '''
        Function triggered upon camera_feed.
        Cannot cv.imshow on this function (gui functions can't be run on a separate thread)
        '''
        pix_fmt = self.camera_config.get('pixel_format', None)
        # convert frame
        if pix_fmt == 'BayerRG8':
            frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_GR2RGB)
        elif pix_fmt == 'RGB':
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        elif pix_fmt == 'gray':
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # resize frame
        self.frame = cv2.resize(frame, (int(frame.shape[1] * self.scale), int(frame.shape[0] * self.scale)))

    def loop(self):
        if self.frame is not None:
            if self.focus:
                gaussian = cv2.GaussianBlur(self.frame, (3, 3), 0)
                laplace = cv2.Laplacian(gaussian, cv2.CV_64F).astype(np.uint8)
                cv2.imshow(f'focus_viewer:{self.camera_feed}', laplace)

            cv2.imshow(f'camera_viewer:{self.camera_feed}', self.frame)
            cv2.waitKey(1)

    def on_stop(self):
        cv2.destroyAllWindows()
        if self.re:
            self.re.stop()
        self.re = None
