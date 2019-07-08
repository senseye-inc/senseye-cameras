import logging

from . output import Output

log = logging.getLogger(__name__)


class VideoRaw(Output):
    '''
    Records raw video using python file IO.
    Writes to a temp file.
    Renames the temp file once recording is done.

    Args:
        path (str): Output path of video.
    '''

    def __init__(self, path=None, **kwargs):
        Output.__init__(self, path=path)

        try:
            self.output = open(self.tmp_path, 'bw')
        except Exception as e:
            log.error(f'Failed to initialize recorder: {self.tmp_path} with exception: {e}.')

    def write(self, frame=None):
        if frame is not None and self.output:
            try:
                self.output.write(frame)

                if 'res' not in self.config:
                    self.config['res'] = frame.shape
            except: pass

    def close(self):
        '''Closes file handle and renames tmp file.'''
        if self.output:
            self.output.close()
            Output.close(self)
        self.output = None
