import logging
from pathlib import Path
from subprocess import Popen, PIPE

from . recorder import Recorder

log = logging.getLogger(__name__)


class FfmpegBayerRecorder(Recorder):
    '''
    Records compressed video using ffmpeg.
    Splits bayer video into 4 streams: 2 green, 1 red, 1 blue.
    Compressess using ffv1.
    '''

    def __init__(self, path=None, config={}):
        Recorder.__init__(self, path=path)

        self.configure(config=config)
        Path(self.path).mkdir(parents=True, exist_ok=True)

        self.bayer_channels = ['g1', 'r', 'b', 'g2']

        for c in self.bayer_channels:
            file_path = str(Path(self.path, f'{c}.avi'))
            Path(file_path).touch()
            process = Popen(f'ffmpeg -hide_banner -loglevel panic -y -f rawvideo -pix_fmt gray -s {self.res} -r {self.fps} -i - -an -c:v ffv1 -g 1 {file_path}'.split(), stdin=PIPE)
            setattr(self, c, process)

            log.info(f"FfmpegBayerRecorder writing to {file_path}")

    def configure(self, config={}):
        for k, v in config.items():
            setattr(self, k, v)

        self.defaults = {
            'fps': 60,
            'res': '900x900',
        }

        for k, v in self.defaults.items():
            if not hasattr(self, k):
                setattr(self, k, v)
                log.warning(f'{k} not set, defaulting to {self.defaults.get(k)}')

    def bayer_frame(self, frame=None, channel=None):
        if channel == 'g1':
            return frame[0::2,0::2]
        elif channel == 'r':
            return frame[0::2,1::2]
        elif channel == 'b':
            return frame[1::2,0::2]
        elif channel == 'g2':
            return frame[1::2,1::2]

    def write(self, frame=None):
        try:
            for c in self.bayer_channels:
                getattr(self, c).stdin.write(self.bayer_frame(frame, c).tostring())
        except BrokenPipeError:
            # occurs if we try to write frames after our processes are closed
            # will occur naturally - a few frames lost aren't an issue.
            pass
        except Exception as e:
            print(e)

    def close(self):
        for c in self.bayer_channels:
            getattr(self, c).kill()
