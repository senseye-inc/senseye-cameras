        # cmd = f'ffmpeg -hide_banner -loglevel panic -y -f rawvideo -pixel_format bgr24 -s {frame_shape[1]}x{frame_shape[0]} -framerate {self.fps} -i - -an -c:v huffyuv -threads 2 {self.file_path}'

import logging
from pathlib import Path
from subprocess import PIPE, Popen, DEVNULL

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

        self.fps = 30

        # set path variables
        # create parent directories if needed
        self.path = Path(path).absolute()

        # TODO: either force avi, or add support for other containers.
        if Path(self.path).suffix != '.avi':
            log.warning('Currently only the ".avi" container is supported. Recording to a non ".avi" container will most likely not work.')

        if self.path.exists():
            log.warning(f'{self.path} exists, overriding')
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

        # recorder vars
        self.process = None
        self.recorder = None


    def initialize_recorder(self, frame=None):
        '''
        Ffmpeg requires us to pass in frame size.
        Thus, we must have a frame to initialize our recorder.
        '''
        try:
            cmd = (
                f'ffmpeg  -hide_banner -loglevel panic -y -f rawvideo -pixel_format bgr24 -s {frame.shape[1]}x{frame.shape[0]} -framerate {self.fps} -i - -an -c:v huffyuv -threads 2 {self.path}'
            )
            self.process = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
            self.recorder = self.process.stdin
            log.info(f'Recording to file: {self.path}')
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
