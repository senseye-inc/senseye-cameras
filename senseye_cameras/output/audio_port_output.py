'''
Script that contains code to read audio from a stream
Author: Jacob Schofield (jacob.schofield@senseye.co) - May 2019
'''

import logging
try:
    import soundfile as sf
except:
    sf = None

from . output import Output
log = logging.getLogger(__name__)


class AudioPortOutput(Output):
    '''Records audio from an input source to a file'''

    def __init__(self, path=None, config={}):

        defaults = {
            'samplerate': 44100,
            'channels': 1,
            'subtype': 'PCM_24',
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
        def __init__(self, *args, **kargs):
            Output.__init__(self)
            log.error("SoundFile not found")
