from senseye_cameras import create_input

USB_VIDEO = './tests/resources/usb_video.mp4'


def test_usb_camera_open_close():
    cam = create_input(type='usb', id=USB_VIDEO)
    cam.open()

    assert cam.input.isOpened()

    cam.close()
    assert cam.input is None


def test_usb_camera_read():
    cam = create_input(type='usb', id=USB_VIDEO)
    cam.open()

    frame, timestamp = cam.read()
    assert frame is not None

    cam.close()
