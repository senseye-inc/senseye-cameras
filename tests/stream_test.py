import os
import time
import shutil

from utils import SAMPLE_RAW_VIDEO, SAMPLE_VIDEO, TMP_DIR, get_tmp_file
from senseye_cameras import Stream

TMP_VIDEO = get_tmp_file(extension='.raw')


def test_stream_raw_video():
    '''Create a raw video to raw video stream.'''
    s = Stream(
        input_type='raw_video', input_config={'res': (1280, 720)}, id=SAMPLE_RAW_VIDEO,
        output_type='raw', path=TMP_VIDEO,
        reading=True, writing=True,
    )
    s.start()

    time.sleep(2)

    s.stop()

    assert os.stat(TMP_VIDEO).st_size > 0
    assert os.stat(TMP_VIDEO).st_size == os.stat(SAMPLE_RAW_VIDEO).st_size
    shutil.rmtree(TMP_DIR)

def test_stream_usb_video():
    s = Stream(
        input_type='usb', id=SAMPLE_VIDEO,
        output_type='raw', path=TMP_VIDEO,
        reading=True, writing=True,
    )
    s.start()

    time.sleep(2)

    s.stop()

    assert os.stat(TMP_VIDEO).st_size > 0
    shutil.rmtree(TMP_DIR)

def test_stream_video_override():
    '''Ensure that streams do not override video files.'''
    s = Stream(
        input_type='usb', id=SAMPLE_VIDEO, input_config={'fps': 10},
        output_type='raw', path=TMP_VIDEO,
        reading=False, writing=False,
    )
    s.start()

    s.start_reading()
    s.start_writing()
    time.sleep(2)
    s.stop_writing()
    s.stop_reading()

    time.sleep(1)

    s.start_reading()
    s.start_writing()
    tmp_path = s.writer.output.tmp_path
    time.sleep(2)
    s.stop_writing()
    s.stop_reading()

    s.stop()

    assert os.stat(TMP_VIDEO).st_size > 0
    assert os.stat(tmp_path).st_size > 0
    shutil.rmtree(TMP_DIR)
