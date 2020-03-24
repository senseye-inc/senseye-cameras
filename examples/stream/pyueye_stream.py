import time
import cv2
from senseye_cameras import Stream

'''
Example pyueye stream.
'''

SLEEP_TIME = 5
CAMERA_ID = 0
FILE_PATH = './tmp/usb.mkv'

# enable live preview of pyueye
def on_frame_read(data, timestamp):
    cv2.imshow('wow', data)
    cv2.waitKey(1)

s = Stream(
    input_type='ueye', id=CAMERA_ID, input_config={
        'fps': 60,
        'exposure': 60,
        'autofocus': 1,
        'autogain': 1,
        'focus_min': 100,
        'focus_max': 200,
    },
    on_read=on_frame_read,

    output_type='file', path=FILE_PATH,
    reading=True,
    writing=True,
)

time.sleep(SLEEP_TIME)

s.stop()
