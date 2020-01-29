import os
import time
import shutil
import nose.tools as nt

from senseye_cameras import Stream

USB_VIDEO = './tests/resources/usb_video.mp4'
RAW_VIDEO = './tests/resources/raw_video.raw'
TMP_VIDEO = './tests/resources/tmp/tmp.raw'
TMP_DIR = './tests/resources/tmp'


def test_stream_raw_video():
    '''Create a raw video to raw video stream.'''
    s = Stream(
        input_type='raw_video', input_config={'res': (1280, 720)}, id=RAW_VIDEO,
        output_type='raw', path=TMP_VIDEO,
        reading=True, writing=True,
    )
    s.start()

    time.sleep(2)

    s.stop()

    nt.assert_greater(os.stat(TMP_VIDEO).st_size, 0)
    nt.assert_equal(os.stat(TMP_VIDEO).st_size, os.stat(RAW_VIDEO).st_size)
    shutil.rmtree(TMP_DIR)

def test_stream_usb_video():
    s = Stream(
        input_type='usb', id=USB_VIDEO,
        output_type='raw', path=TMP_VIDEO,
        reading=True, writing=True,
    )
    s.start()

    time.sleep(2)

    s.stop()

    nt.assert_greater(os.stat(TMP_VIDEO).st_size, 0)
    shutil.rmtree(TMP_DIR)

def test_stream_video_override():
    '''Ensure that streams do not override video files.'''
    s = Stream(
        input_type='usb', id=USB_VIDEO, input_config={'fps': 10},
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

    nt.assert_greater(os.stat(TMP_VIDEO).st_size, 0)
    nt.assert_greater(os.stat(tmp_path).st_size, 0)
    shutil.rmtree(TMP_DIR)
