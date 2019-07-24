import time
from resources import config
from senseye_cameras import Stream

s = Stream(
    input_type='emergent',
    output_type='video_emergent', path='./tmp/emergent.raw',
    reading=True, writing=True,
)
s.start()

time.sleep(10)

s.stop()
