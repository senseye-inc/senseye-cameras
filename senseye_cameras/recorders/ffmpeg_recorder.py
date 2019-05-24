import logging
from pathlib import Path
from subprocess import PIPE, Popen, DEVNULL

from .. utils import configure, ffmpeg_string
from . recorder import Recorder

log = logging.getLogger(__name__)


class FfmpegRecorder(Recorder):
    '''
    Records raw video using python file IO.
    Writes to a temp file.
    Renames the temp file once recording is done.
    '''

    def __init__(self, path=None, config={}):
        Recorder.__init__(self, path=path)

        # configuration
        self.defaults = {
            'fps': 30,
            'pixel_format': 'rgb24',
            'codec': 'huffyuv',
            'format': 'rawvideo',
        }
        self.config = {**self.defaults, **config}

        self.process = None
        self.recorder = None

    def initialize_recorder(self, frame=None):
        '''
        Ffmpeg requires us to pass in frame size.
        Thus, we must have a frame to initialize our recorder.
        '''
        try:
            cmd = ffmpeg_string(path=self.path, res=(frame.shape[1], frame.shape[0]), **self.config)
            self.process = Popen(cmd.split(), stdin=PIPE)
            self.recorder = self.process.stdin
            self.log_record_start()
        except Exception as e:
            log.error(f'Failed to initialize recorder: {self.path} with exception: {e}.')

    def write(self, frame=None):
        if frame is None:
            return

        if self.recorder is None:
            self.initialize_recorder(frame=frame)

        try:
            self.recorder.write(frame)
        except: pass

    def close(self):
        '''
        Closes ffmpeg process.
        Renames tmp file.
        '''
        if self.process:
            self.process.kill()
            self.process.communicate()
            self.process = None
            self.recorder = None

            # TODO: iterate on this. do we need to write on a tmp file?
            log.info(f'Recording complete: {self.path}')
