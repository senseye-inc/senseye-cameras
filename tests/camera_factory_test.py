import nose.tools as nt

from senseye_cameras import create_input

USB_VIDEO = './tests/resources/usb_video.mp4'


def test_create_usb_camera():
    cam = create_input(type='usb', id=USB_VIDEO)
    cam.open()

    nt.assert_true(cam.input.isOpened())

    frame, timestamp = cam.read()
    nt.assert_is_not_none(frame)


    cam.close()
    nt.assert_is_none(cam.input)
