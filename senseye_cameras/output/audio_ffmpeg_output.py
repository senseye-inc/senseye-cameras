import logging
from subprocess import Popen, PIPE

from . output import Output

log = logging.getLogger(__name__)


class AudioFfmpegOutput(Output):
    '''
    Writes audio to an ffmpeg process.
    Args:
        path (str): Output path of video.
        config (dict): Configuration dictionary. Accepted keywords:
            channels (int): number of audio channels
            samplerate (int): audio sample rate
            format (str): audio codec
    '''

    def __init__(self, path=None, config={}):
        defaults = {
            'channels': 2,
            'samplerate': 44100,
            'format': 's32le',
        }
        Output.__init__(self, path=path, config=config, defaults=defaults)

        self.cmd = (
            f'ffmpeg '
            f'-y '
            f'-f {self.config["format"]} '
            f'-ac {self.config["channels"]} '
            f'-ar {self.config["samplerate"]} '
            f'-i - '
            f'{self.tmp_path}'
        )
        self.process = Popen(self.cmd, shell=True, stdin=PIPE)
        self.output = self.process.stdin

    def write(self, data=None):
        if data is not None:
            try:
                self.output.write(data)
            except: pass

    def close(self):
        if self.process:
            if self.process.poll() == None:
                self.process.communicate()
            Output.close(self)

        self.process = None
        self.output = None
