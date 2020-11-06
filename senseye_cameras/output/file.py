import ffmpeg
import logging
import tempfile
from pathlib import Path

from . output import Output

log = logging.getLogger(__name__)


class File(Output):
    '''
    Records to a file.
    Automatically detects the correct codec to use based on the path suffix.
    Supports suffixes: '.avi', '.mp4', '.mkv', '.yuv', '.raw'

    Args:
        path (str): Output path of video.
        config (dict): Configuration dictionary. Accepted keywords:
            fps (int)
            pixel_format (str): pixel format of the incoming raw video
            codec (str)
            format (str): defaults to 'rawvideo'
            res (tuple)
    '''

    def __init__(self, path=None, **kwargs):
        defaults = {
            'fps': 30,
            'format': 'rawvideo',
            'pixel_format': 'rgb24',
            'output_pixel_format': 'rgb24',
            'file_codec': {},
            'res': (1280, 720)
        }
        Output.__init__(self, defaults=defaults, **kwargs)

        self.process = None

        self.set_path(path=path)
        self.set_tmp_path(path=self.path)

        if Path(self.path).suffix == '.raw':
            self.output = open(self.tmp_path, 'bw')
        else:
            self.generate_file_codec()
            self.initialize_ffmpeg()

    def generate_file_codec(self):
        '''Determines a good codec to use based on path.suffix.'''
        codec_lookup = {
            '.avi': {'vcodec': 'huffyuv'},
            '.mp4': {'vcodec': 'libx264', 'crf': 17, 'preset': 'ultrafast'},
            '.mkv': {'vcodec': 'h264', 'crf': 23, 'preset': 'ultrafast'},
            '.yuv': {'vcodec': 'rawvideo'}
        }

        suffix = Path(self.path).suffix
        self.config['file_codec'] = codec_lookup.get(suffix, None)
        if self.config['file_codec'] is None:
            raise Exception(f'File extension {suffix} not supported.')

    def initialize_ffmpeg(self):
        '''Initializes ffmpeg.'''
        # only include pixel_format and size if we're encoding raw video.
        raw_args = dict(
            pix_fmt=self.config.get('pixel_format'),
            s=f'{self.config.get("res")[0]}x{self.config.get("res")[1]}'
        ) if self.config['format'] == 'rawvideo' else {}

        self.process = (
            ffmpeg
            .input(
                'pipe:',
                format=self.config.get('format'),
                framerate=self.config.get('fps'),
                **raw_args
            )
            .output(
                self.tmp_path,
                **self.config.get('file_codec'),
            )
            # hide logging
            .global_args('-loglevel', 'error', '-hide_banner')
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        log.info(f'Running command: {" ".join(self.process.args)}')
        self.output = self.process.stdin

    def set_path(self, path=None):
        '''Setter for self.path.'''
        self.path = Path(path).absolute()
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    def set_tmp_path(self, path):
        '''Generates a tmpfile name in 'path's directory.'''
        path = Path(path)
        self.tmp_path = tempfile.NamedTemporaryFile(
            prefix=path.stem,
            dir=path.parent,
            suffix=path.suffix,
            delete=True
        ).name

        log.debug(f'{str(self)} tmp path set to {self.tmp_path}')

    def write(self, data=None):
        if data is not None and self.output:
            try:
                self.output.write(data)
            except: pass

    def close(self):
        if self.output:
            if self.process and self.process.poll() == None:
                try:
                    self.process.communicate(timeout=5)
                except Exception as e:
                    log.warning(f'Failed to end process cleanly with error {e}. Killing...')
                    self.process.kill()
                    outs, errs = self.process.communicate()
                    log.error(f'Process kill results: {errs}')

            try:
                # make the stream reusable by creating a new tmp path
                old_tmp_path = self.tmp_path
                self.set_tmp_path(self.path)
                if self.path.exists():
                    raise Exception(f'Rename from {old_tmp_path} to {self.path} failed, {self.path} already exists.')
                Path(old_tmp_path).replace(self.path)
            except Exception as e:
                log.error(f'Recording rename failed: {e}')
            Output.close(self)
        self.output = None
