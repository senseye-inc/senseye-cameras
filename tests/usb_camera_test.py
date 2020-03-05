from senseye_cameras import create_input
from utils import SAMPLE_VIDEO


def test_usb_camera_open_close():
    cam = create_input(type='usb', id=SAMPLE_VIDEO)
    cam.open()

    assert cam.input.isOpened()

    cam.close()
    assert cam.input is None


def test_usb_camera_read():
    cam = create_input(type='usb', id=SAMPLE_VIDEO)
    cam.open()

    frame, timestamp = cam.read()
    assert frame is not None

    cam.close()
