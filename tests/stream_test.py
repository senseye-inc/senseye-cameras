import os
import time
import nose.tools as nt

from senseye_cameras import Stream

USB_VIDEO = './tests/resources/usb_video.mp4'
RAW_VIDEO = './tests/resources/raw_video.raw'
TMP_VIDEO = './tests/resources/tmp.raw'


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
    os.remove(TMP_VIDEO)

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
    os.remove(TMP_VIDEO)
