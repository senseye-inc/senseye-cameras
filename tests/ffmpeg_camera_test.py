import logging
from senseye_cameras import create_input

CAMERA_TYPE = 'ffmpeg'
CAMERA_ID = 0

log = logging.getLogger(__name__)


def test_ffmpeg_camera_read():
    '''
    Test reading from an ffmpeg camera.
    cam.open() will only run successfully if:
        1. ffmpeg binaries on the system path
        2. A camera ffmpeg can access.
    Thus, only run the test if camera.open() does not fail.
    '''
    cam = None
    try:
        cam = create_input(type=CAMERA_TYPE, id=CAMERA_ID)
        cam.open()
    except Exception as e:
        log.warning(f'Test could not be run, camera open failed with error: {e}')

    if cam.input:
        frame, timestamp = cam.read()
        assert frame is not None

        cam.close()
