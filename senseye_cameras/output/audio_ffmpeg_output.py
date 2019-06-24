import logging
import numpy as np
from subprocess import Popen, PIPE

from senseye_utils.date_utils import timestamp_now

from . output import Output

log = logging.getLogger(__name__)


class AudioFfmpegOutput(Output):
    '''
    Treats raw video as a camera.
    Args:
        id (str): path to the raw video file.
        config (dict): Configuration dictionary. Accepted keywords:
            res (tuple): frame size
    '''

    def __init__(self, path=None, config={}):
        defaults = {
            'channels': 2,
            'format': 's32le',
            'rate': 44100,
        }
        Output.__init__(self, path=path, config=config, defaults=defaults)

        self.cmd = (
            f'ffmpeg '
            f'-y '
            f'-f {self.config["format"]} '
            f'-ac {self.config["channels"]} '
            f'-ar {self.config["rate"]} '
            f'-i - '
            f'{self.tmp_path}'
        )

        self.process = Popen(self.cmd, shell=True, stdin=PIPE)
        self.output = self.process.stdin

    def write(self, data=None):
        if data is None:
            return

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
