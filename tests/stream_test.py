import os
import time
from utils import SAMPLE_VIDEO, get_tmp_file, rm_tmp_dir
from senseye_cameras import Stream



def test_stream_video_override():
    '''Ensure that streams do not override video files.'''
    TMP_FILE = get_tmp_file(extension='.raw')
    s = Stream(
        input_type='usb', id=SAMPLE_VIDEO, input_config={'fps': 10},
        output_type='raw', path=TMP_FILE,
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

    assert os.stat(TMP_FILE).st_size > 0
    assert os.stat(tmp_path).st_size > 0
    rm_tmp_dir()
