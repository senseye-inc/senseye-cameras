import nose.tools as nt

from senseye_cameras import create_input

USB_VIDEO = './tests/resources/usb_video.mp4'


def test_usb_camera_open_close():
    cam = create_input(type='usb', id=USB_VIDEO)
    cam.open()

    nt.assert_true(cam.input.isOpened())

    cam.close()
    nt.assert_is_none(cam.input)


def test_usb_camera_read():
    cam = create_input(type='usb', id=USB_VIDEO)
    cam.open()

    frame, timestamp = cam.read()
    nt.assert_is_not_none(frame, None)

    cam.close()
