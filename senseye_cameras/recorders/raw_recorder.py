import logging
import tempfile
from pathlib import Path

from . recorder import Recorder

log = logging.getLogger(__name__)


class RawRecorder(Recorder):
    '''
    Records raw video using python file IO.
    Writes to a temp file.
    Renames the temp file once recording is done.

    Args:
        path (str): Output path of video.
    '''

    def __init__(self, path=None, **kwargs):
        Recorder.__init__(self, path=path)

        try:
            self.recorder = open(self.tmp_path, 'bw')
            self.log_start()
        except Exception as e:
            log.error(f'Failed to initialize recorder: {self.tmp_path} with exception: {e}.')

    def write(self, frame=None):
        if frame is not None and self.recorder:
            try:
                self.recorder.write(frame)

                if 'res' not in self.config:
                    self.config['res'] = frame.shape
            except: pass

    def close(self):
        '''
        Closes file handle.
        Renames tmp file.
        '''
        if self.recorder:
            self.recorder.close()
            self.recorder = None

            Recorder.close(self)
