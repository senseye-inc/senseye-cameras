import logging

from senseye_utils import LoopThread
from . camera_reader import CameraReader
from . camera_writer import CameraWriter

log = logging.getLogger(__name__)


class CameraHandler(LoopThread):
    '''
    Links camera_reader and writer.
    Writes frames to disk immediately without going through ZMQ.
    '''
    def __init__(self, camera_feed=None, viewer=False,
        camera_type='usb', camera_config={}, camera_id=0,
        recorder_type='raw', recorder_config={}, path=None,
    ):
        self.reader = CameraReader(
            camera_feed=camera_feed,
            camera_type=camera_type,
            camera_config=camera_config,
            camera_id=camera_id,
        )

        self.writer = CameraWriter(
            camera_feed=camera_feed,
            recorder_type=recorder_type,
            recorder_config=recorder_config,
            path=path,
        )

        LoopThread.__init__(self, frequency=self.reader.frequency)

    def loop(self):
        frame, timestamp = self.reader.camera.read()
        if frame is not None:
            self.writer.recorder.write(frame)
            self.reader.re.publish(self.reader.camera_feed, frame=frame, timestamp=timestamp)

    def on_start(self):
        self.reader.on_start()

    def on_stop(self):
        self.reader.on_stop()
        self.writer.on_stop()
