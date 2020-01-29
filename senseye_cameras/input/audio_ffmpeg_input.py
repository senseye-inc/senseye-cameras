import os
import time
import logging
from subprocess import Popen, PIPE, STDOUT

from . input import Input

log = logging.getLogger(__name__)


class AudioFfmpegInput(Input):
    '''
    Reads in audio using ffmpeg.
    Args:
        id (str): audio device index
        config (dict): Configuration dictionary. Accepted keywords:
            channels (int): number of audio channels
            block_size (int): number of bytes to read in per iteration
            samplerate (int): audio sample rate
            format (str): audio codec
    '''

    def __init__(self, id=0, config={}):
        defaults = {
            'channels': 2,
            'block_size': 64,
            'samplerate': 44100,
            'format': 's32le',
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

        if os.name == 'nt':
            format = 'dshow'
            device = f'audio={self.get_dshow_audio_device(self.id)}'
        else:
            device = f':{self.id}'
            format = 'avfoundation'

        self.cmd = (
            f'ffmpeg '
            f'-f {format} '
            f'-ac {self.config["channels"]} '
            f'-i {device} '
            f'-f {self.config["format"]} '
            f'-'
        )

    def get_dshow_audio_device(self, id):
        # get ffmpeg list device output
        cmd = 'ffmpeg -hide_banner -f dshow -list_devices true -i -'
        process = Popen(cmd.split(), universal_newlines=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
        output = process.communicate()[0]

        try:
            # only show audio devices
            audio = output[output.find('DirectShow audio devices'):]
            # get the first audio device
            device = audio.split('\n')[id + 1]
            # strip whitespace
            device = device[device.find(']') + 1:].strip()
            return device
        except:
            log.warning("Failed to find dshow audio device.")
        return ''

    def open(self):
        self.process = Popen(self.cmd, shell=True, stdout=PIPE, stderr=PIPE)
        self.input = self.process.stdout

    def read(self):
        return self.input.read(self.config['block_size']), time.time()

    def close(self):
        if self.process:
            self.process.kill()
        self.input = None
        self.process = None
