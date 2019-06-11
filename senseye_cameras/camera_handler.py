import logging

from senseye_utils import LoopThread, RapidEvents
from . cameras.camera_factory import create_camera
from . recorders.recorder_factory import create_recorder

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
    def __init__(self, camera_feed=None,
        camera_type='usb', camera_config={}, camera_id=0,
        recorder_type='raw', recorder_config={}, path=None,
    ):
        self.camera_feed = camera_feed

        self.camera = create_camera(camera_type=camera_type, config=camera_config, id=camera_id)
        self.recorder = create_recorder(recorder_type=recorder_type, path=path, config=recorder_config)

        self.reading = False
        self.writing = False

        self.re = RapidEvents(f'camera_handler:{camera_type}:{camera_id}:{recorder_type}')

        LoopThread.__init__(self, frequency=camera_config.get('fps', -1))

    def set_path(self, path=None):
        log.info(f'Recorder path set to {path}')
        self.recorder.set_path(path)

    def start_reading(self):
        log.info(f'Camera reading.')
        self.camera.open()
        self.reading = True

    def start_writing(self):
        log.info('Recorder writing.')
        self.writing = True

    def stop_reading(self):
        log.info(f'Camera closing.')
        self.reading = False
        if self.camera:
            self.camera.close()

    def stop_writing(self):
        log.info('Recorder closing.')
        self.writing = False
        if self.recorder:
            self.recorder.close()

    def on_stop(self):
        self.stop_reading()
        self.start_writing()

    def loop(self):
        if self.reading:
            frame, timestamp = self.camera.read()
            if frame is not None:
                self.re.publish(self.camera_feed, frame=frame, timestamp=timestamp)
                if self.writing:
                    self.recorder.write(frame)
