import os
import time
import logging
from utils import get_tmp_file, rm_tmp_dir
from senseye_cameras import create_input, Stream

CAMERA_TYPE = 'ffmpeg'
CAMERA_ID = 0

log = logging.getLogger(__name__)


def test_read():
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
        log.warning(f'Test could not be run, camera open failed with error: {e}. This is most likely a hardware issue.')
        return

    frame, timestamp = cam.read()
    assert frame is not None

    cam.close()

def test_stream():
    '''
    Test an ffmeg stream: ffmpeg -> file
    '''
    try:
        s = Stream(
            input_type='ffmpeg', id=0,
            output_type='file', path=get_tmp_file(),
            reading=True, writing=True,
        )
    except Exception as e:
        log.warning(f'Test could not be run, stream initialization failed with error: {e}. This is most likely a hardware issue.')
        return

    time.sleep(2)

    s.stop()

    assert os.stat(get_tmp_file()).st_size > 0
    rm_tmp_dir()
