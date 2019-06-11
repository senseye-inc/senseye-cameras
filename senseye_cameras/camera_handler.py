import logging

from senseye_utils import LoopThread
from . camera_reader import CameraReader
from . camera_writer import CameraWriter

log = logging.getLogger(__name__)


class CameraHandler(LoopThread):
    '''
    Links camera_reader and camera_writer.
    Writes frames to disk immediately without going through ZMQ.

    Args:
        camera_feed (str): RapidEvents channel where frames are published.
        viewer (bool): Whether to display read in frames.

        camera_type (str): See create_camera.
        camera_config (dict)
        camera_id (str OR int)

        recorder_type (str): See create_recorder.
        recorder_config (str)
        path (str): file frames are written to.
    '''
    def __init__(self, camera_feed=None, viewer=False,
        camera_type='usb', camera_config={}, camera_id=0,
        recorder_type='raw', recorder_config={}, path=None,
    ):
        self.camera_feed = camera_feed
        self.viewer = viewer
        self.camera_type = camera_type
        self.camera_config = camera_config
        self.camera_id = camera_id
        self.recorder_type = recorder_type
        self.recorder_config = recorder_config
        self.path = path

        self.reader = None
        self.writer = None

        LoopThread.__init__(self, frequency=camera_config.get('fps', -1))

    def initialize_writer(self):
        if self.writer is None:
            self.writer = CameraWriter(
                camera_feed=self.camera_feed,
                recorder_type=self.recorder_type,
                recorder_config=self.recorder_config,
                path=self.path,
            )

    def initialize_reader(self):
        if self.reader is None:
            self.reader = CameraReader(
                camera_feed=self.camera_feed,
                camera_type=self.camera_type,
                camera_config=self.camera_config,
                camera_id=self.camera_id,
            )

    def start_reader(self):
        self.initialize_reader()
        self.reader.on_start()

    def start_writer(self):
        self.initialize_writer()

    def stop_reader(self):
        if self.reader:
            self.reader.stop()
        self.reader = None

    def stop_writer(self):
        self.writer.on_stop()
        self.writer = None

    def on_stop(self):
        self.stop_reader()
        self.stop_writer()

    def set_path(self, path=None):
        self.initialize_writer()
        self.writer.set_path(path=path)

    def loop(self):
        if self.reader:
            frame, timestamp = self.reader.camera.read()
            if self.writer and frame is not None:
                self.writer.recorder.write(frame)
                self.reader.re.publish(self.reader.camera_feed, frame=frame, timestamp=timestamp)
