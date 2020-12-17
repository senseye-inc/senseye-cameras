import logging
from senseye_cameras import create_input

log = logging.getLogger(__name__)


def test_read():
    '''
    Test reading from an pylon camera.
    cam.open() will only run successfully if:
        1. the pylon sdk is installed
        2. pypylon is installed
        3. a pylon camera is connected
    Thus, only run the test if camera.open() does not fail.
    '''
    cam = None
    frame = None
    try:
        cam = create_input(type='pylon', id=0)
        cam.open()
        frame, timestamp = cam.read()
    except Exception as e:
        log.warning(f'Test could not be run, camera open failed with error: {e}')
        return

    assert frame is not None

    cam.close()
