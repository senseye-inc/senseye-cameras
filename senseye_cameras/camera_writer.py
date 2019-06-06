import logging

from senseye_utils import LoopThread, SafeQueue, RapidEvents

from . recorders.recorder_factory import create_recorder

log = logging.getLogger(__name__)


class CameraWriter(LoopThread):
    '''
    Listens for and writes frames to disk.
    Args:
        camera_feed (str): RapidEvent channel that this object listens to for frames
        recorder_type (str): see 'create_recorder' documentation.
        recorder_config (dict): configures the recorder.
        path (str): file frames are written to.
    '''

    def __init__(self, camera_feed=None, recorder_type='raw', recorder_config={}, path=None):
        LoopThread.__init__(self, frequency=150)

        self.recorder = create_recorder(recorder_type=recorder_type, path=path, config=recorder_config)
        self.frame_q = SafeQueue(100)
        self.path = path

        self.re = None
        self.camera_feed = camera_feed

    def set_path(self, path=None):
        self.recorder.set_path(path)

    def on_start(self):
        '''
        Initialize RapidEvents object.
        '''
        self.re = RapidEvents(f'camera_writer:{self.path}')
        self.re.connect(self.on_frame_read, self.camera_feed)
        log.info(f"Creating camera writer. Listening to {self.camera_feed}")

    def on_frame_read(self, frame=None):
        '''
        Appends frames to a queue upon receiving a frame_read event.
        '''
        if frame is not None:
            self.frame_q.put_nowait(frame)

    def on_stop(self):
        '''
        Cleans up our recorder and RapidEvents instances.
        '''
        if self.recorder:
            self.recorder.close()
            self.recorder = None

        if self.re:
            self.re.stop()
            self.re = None

    def loop(self):
        '''
        Transfers frames from frame_q to disk.
        '''
        frame = self.frame_q.get_nowait()
        if self.recorder and frame is not None:
            self.recorder.write(frame)
