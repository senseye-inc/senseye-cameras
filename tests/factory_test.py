from senseye_cameras import create_input
from utils import SAMPLE_RAW_VIDEO, SAMPLE_VIDEO

def try_camera(type, id):
    '''Tries to open and read from a camera.'''
    cam = create_input(type=type, id=id)
    cam.open()

    frame, timestamp = cam.read()
    assert frame is not None

    cam.close()
    assert cam.input is None

def test_create_usb_camera():
    try_camera('usb', SAMPLE_VIDEO)

def test_create_raw_camera():
    try_camera('raw_video', SAMPLE_RAW_VIDEO)
