import os
import logging
import signal
from subprocess import Popen, PIPE, STDOUT
from . recorder import Recorder

log = logging.getLogger(__name__)


class FfmpegAudio(Recorder):
    '''
    Records raw video using python file IO.
    Writes to a temp file.
    Renames the temp file once recording is done.

    Args:
        path (str): Output path of video.
    '''

    def __init__(self, path=None, config={}):
        Recorder.__init__(self, path=path, suffix='.mp3')

        self.generate_cmd()

    def generate_cmd(self):
        if os.name == 'posix':
            self.cmd = f'ffmpeg -f avfoundation -hide_banner -loglevel warning -y -i ":0" {self.tmp_path}'
        else:
            audio_device = self.get_first_dshow_audio_device()
            self.cmd = f'ffmpeg -f dshow -i audio={audio_device} {self.tmp_path}'


    def get_first_dshow_audio_device(self):
        # get ffmpeg list device output
        cmd = 'ffmpeg -hide_banner -f dshow -list_devices true -i -'
        process = Popen(cmd.split(), universal_newlines=True, stdout=PIPE, stderr=STDOUT)
        output = process.communicate()[0]

        try:
            # only show audio devices
            audio = output[output.find('DirectShow audio devices'):]
            # get the first audio device
            device = audio.split('\n')[1]
            # strip whitespace
            device = device[device.find(']') + 1:].strip()
            return device
        except:
            log.warning("Failed to find dshow audio device.")
        return ''

    def open(self):
        self.process = Popen(self.cmd, shell=True)

    def close(self):
        '''
        Closes file handle.
        Renames tmp file.
        '''
        if self.process:
            os.kill(self.process.pid, signal.SIGINT)
            self.process = None
            self.recorder = None

            Recorder.close(self)
