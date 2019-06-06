import nose.tools as nt

from senseye_cameras import create_camera

USB_VIDEO = './tests/resources/usb_video.mp4'


def test_create_usb_camera():
    cam = create_camera(camera_type='usb', id=USB_VIDEO)
    cam.open()

    nt.assert_true(cam.camera.isOpened())

    frame, timestamp = cam.read()
    nt.assert_is_not_none(frame)


    cam.close()
    nt.assert_is_none(cam.camera)
