import logging

try:
    import soundfile as sf
except:
    sf = None

from . output import Output
log = logging.getLogger(__name__)


class AudioPortOutput(Output):
    '''
    Writes audio to a file using soundfile.
    Args:
        path (str): Output path of video.
        config (dict): Configuration dictionary. Accepted keywords:
            channels (int): number of audio channels
            samplerate (int): audio sample rate
            subtype (str): audio type
    '''

    def __init__(self, path=None, config={}):
        defaults = {
            'channels': 1,
            'samplerate': 44100,
            'subtype': 'PCM_16',
        }
        Output.__init__(self, path=path, config=config, defaults=defaults)

        self.output = sf.SoundFile(
            self.tmp_path,
            mode='w',
            samplerate=self.config['samplerate'],
            channels=self.config['channels'],
            subtype=self.config['subtype']
        )

    def write(self, data=None):
        if data is not None:
            self.output.write(data)

    def close(self):
        if self.output:
            self.output.close()
            Output.close(self)
        self.output = None

if sf is None:
    class AudioPortOutput(Output):
        def __init__(self, path=None, config={}):
            Output.__init__(self, path=path, config=config, defaults={})
