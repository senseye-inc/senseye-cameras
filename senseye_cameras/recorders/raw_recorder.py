import logging
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

        # set path variables
        # create parent directories if needed
        self.path = Path(path).absolute()
        self.tmp_path = Path(f'{self.path}.tmp')

        # warn users if we're about to override some files
        if self.path.exists():
            log.warning(f'{self.path} exists, overriding')
        if self.tmp_path.exists():
            log.warning(f'{self.tmp_path} exists, overriding')
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

        # create recorder
        try:
            self.recorder = open(self.tmp_path, 'bw')
            self.log_record_start()
        except Exception as e:
            log.error(f'Failed to initialize recorder: {self.tmp_path} with exception: {e}.')

    def write(self, frame=None):
        if frame is not None and self.recorder:
            try:
                self.recorder.write(frame)
            except: pass

    def close(self):
        '''
        Closes file handle.
        Renames tmp file.
        '''
        if self.recorder:
            self.recorder.close()
            self.recorder = None

            try:
                Path(self.tmp_path).rename(self.path)
                log.info(f'Recording complete: {self.path}')
            except Exception as e:
                log.error(f'Recording rename failed: {e}')
