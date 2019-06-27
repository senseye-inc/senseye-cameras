import time
from senseye_cameras import Stream

s = Stream(
    input_type='emergent',
    output_type='raw', path='./tmp/emergent.raw',
    reading=True, writing=True,
)
s.start()

time.sleep(5)

s.stop()
