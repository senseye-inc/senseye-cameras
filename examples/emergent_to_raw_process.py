import time
from resources import config
from senseye_cameras import Stream
from senseye_utils import ProcessManager
import multiprocessing as mp

if __name__ == '__main__':
    mp.freeze_support()
    pm = ProcessManager()
    pm.add_process(
        Stream,
        input_type='emergent',
        output_type='video_emergent', path='./tmp/emergent.raw',
        reading=True, writing=True,
    )
    pm.start()
    time.sleep(5)
    pm.stop()
