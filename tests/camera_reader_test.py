import time
import nose.tools as nt

from senseye_cameras import CameraReader
from senseye_utils import RapidEvents

USB_VIDEO = './tests/resources/usb_video.mp4'


def test_camera_reader():
    camera_feed = 'CR_TEST'

    re = RapidEvents('CR_TEST')
    cr = CameraReader(camera_feed=camera_feed, camera_type='video', camera_id=USB_VIDEO)

    def fn(*args, frame=None, **kwargs):
        if frame is not None:
            fn.frames += 1
    fn.frames = 0
    re.connect(fn, camera_feed)

    cr.start()
    time.sleep(2)
    cr.stop()

    nt.assert_greater(fn.frames, 0)
    re.stop()
