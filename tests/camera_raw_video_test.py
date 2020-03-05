import os
import time
from senseye_cameras import create_input, Stream
from utils import SAMPLE_RAW_VIDEO, get_tmp_file, rm_tmp_dir


def test_sanity():
    cam = create_input(type='raw_video', id=SAMPLE_RAW_VIDEO)
    cam.open()

    cam.close()
    assert cam.input is None


def test_read():
    cam = create_input(type='raw_video', id=SAMPLE_RAW_VIDEO)
    cam.open()

    frame, timestamp = cam.read()
    assert frame is not None

    cam.close()

def test_stream():
    '''
    Test an usb stream: usb -> file
    '''
    TMP_FILE = get_tmp_file(extension='.raw')
    s = Stream(
        input_type='raw_video', id=SAMPLE_RAW_VIDEO,
        output_type='file', path=TMP_FILE,
        reading=True, writing=True,
    )

    time.sleep(2)

    s.stop()

    assert os.stat(TMP_FILE).st_size > 0
    rm_tmp_dir()
