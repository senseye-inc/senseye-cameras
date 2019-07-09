'''
Opens an emergent stream.
Attaches a RapidEvents instance to the emergent stream that publishes read frames.
Opens a CameraViewer that listens for frames and displays them using opencv imshow.
'''
import time
from resources import config
from senseye_cameras import Stream, CameraViewer
from senseye_utils import ProcessManager, RapidEvents

class StreamWrapper(Stream):
    def __init__(self, *args, camera_feed=None, **kwargs):
        self.re = RapidEvents('StreamWrapper')

        def on_frame_read(data, timestamp):
            self.re.publish(camera_feed, frame=data, timestamp=timestamp)
        Stream.__init__(self, *args, on_read=on_frame_read, **kwargs)

if __name__ == '__main__':
    CAMERA_FEED='emergent_feed'

    camera_config={
        'res': (2048, 1088),
        'fps': 318,
        'exposure': 2919,
        'gain': 1024,
        'path':'wow.raw',
        'pix_fmt': 'gray',
    }

    pm = ProcessManager()
    pm.add_process(
        StreamWrapper,
        camera_feed=CAMERA_FEED,
        input_type='emergent',
        input_config=camera_config,
        reading=True,
    )

    pm.add_process(
        CameraViewer,
        camera_feed=CAMERA_FEED,
        camera_config=camera_config,
    )

    pm.start()
    time.sleep(50)
    pm.stop()
