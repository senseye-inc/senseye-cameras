import logging
from pathlib import Path
from subprocess import Popen, PIPE

from . recorder import Recorder
from .. utils import ffmpeg_string

log = logging.getLogger(__name__)


class FfmpegBayerRecorder(Recorder):
    '''
    Records compressed video using ffmpeg.
    Splits bayer video into 4 streams: 2 green, 1 red, 1 blue.
    Compressess using ffv1.

    Args:
        path (str): Output path of video.
        config (dict): Configuration dictionary. Accepted keywords:
            fps (int)
            pixel_format (str)
            codec (str)
            format (str)
            res (tuple)
    '''

    def __init__(self, path=None, config={}):
        # Recorder.__init__(self, path=path)/
        self.config = config

        # configuration
        self.defaults = {
            'fps': 30,
            'pixel_format': 'gray',
            'codec': 'ffv1',
            'format': 'rawvideo',
            'res': (900, 900),
        }
        self.config = {**self.defaults, **config}

        Path(self.path).mkdir(parents=True, exist_ok=True)

        # create a Popen ffmpeg process for each bayer_channel
        # assign an attribute to the process object
        # IE self.g1 would point to the ffmpeg process responsible for compressing the bayer g1 channel
        self.bayer_channels = ['g1', 'r', 'b', 'g2']
        for c in self.bayer_channels:
            file_path = str(Path(self.path, f'{c}.avi'))
            Path(file_path).touch()
            cmd = ffmpeg_string(path=file_path, **self.config)
            process = Popen(cmd.split(), stdin=PIPE)
            setattr(self, c, process)
        self.log_record_start()

    def bayer_frame(self, frame=None, channel=None):
        '''
        Split the given frame based on channel given.
        '''
        if channel == 'g1':
            return frame[0::2,0::2]
        elif channel == 'r':
            return frame[0::2,1::2]
        elif channel == 'b':
            return frame[1::2,0::2]
        elif channel == 'g2':
            return frame[1::2,1::2]

    def write(self, frame=None):
        if frame is not None:
            try:
                for c in self.bayer_channels:
                    getattr(self, c).stdin.write(self.bayer_frame(frame, c).tostring())
            except BrokenPipeError:
                # occurs if we try to write frames after our processes are closed
                # will occur naturally - a few frames lost aren't an issue.
                pass
            except Exception as e:
                log.error(f'Ffempg Bayer write error: {e}')

    def close(self):
        for c in self.bayer_channels:
            getattr(self, c).kill()
