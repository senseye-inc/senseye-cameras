import time
from resources import config
from senseye_cameras import Stream

c = {
    'res': (2064,1536),
    'exposure': 'max',
    'fps': 150,
    'gain': 1024,
    'binning': 1,
    'decimation': 3,
}
s = Stream(
    input_config=c,
    input_type='emergent',
    output_type='video_emergent', path='./tmp/emergent.raw',
    reading=True, writing=True,
)
s.start()

time.sleep(5)

s.stop()
