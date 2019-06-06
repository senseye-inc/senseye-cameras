import os
import time
import nose.tools as nt

from senseye_cameras import CameraHandler

USB_VIDEO = './tests/resources/usb_video.mp4'
TMP_VIDEO = './tests/resources/tmp.avi'


def test_camera_handler():
    ch = CameraHandler(
        camera_type='video',
        camera_id=USB_VIDEO,
        recorder_type='raw',
        path=TMP_VIDEO
    )
    ch.start()
    time.sleep(5)
    ch.stop()

    nt.assert_greater(os.stat(TMP_VIDEO).st_size, 0)
    os.remove(TMP_VIDEO)
