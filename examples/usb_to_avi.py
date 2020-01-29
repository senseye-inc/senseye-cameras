import time
from resources import config
from senseye_cameras import Stream

s = Stream(
    input_type='usb', id=0,
    output_type='ffmpeg', path='./tmp/usb.avi',
    reading=True,
)
s.start()

time.sleep(2)

s.start_writing()

time.sleep(5)

s.stop()