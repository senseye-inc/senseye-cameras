"""
Script that contains code to record audio from a webcam
Author: Jacob Schofield (jacob.schofield@senseye.co) - May 2019
"""
import logging
try:
    import sounddevice as sd
except:
    sd = None

from senseye_utils.date_utils import timestamp_now
from . input import Input

log = logging.getLogger(__name__)


class AudioPortInput(Input):
    '''Handles audio recording audio using the sounddevice api for portaudio'''

    def __init__(self, id=0, config={}):

        defaults = {
            'samplerate': 44100,
            'channels': 1,
            'device': id,
            'blocksize': 1024,
        }
        Input.__init__(self, id=id, config=config, defaults=defaults)

    def configure(self):
        '''
        Supported configurations: samplerate, channels, blocksize
        '''
        device_info = sd.query_devices(self.config['device'], 'input')
        if 'samplerate' not in self.config:
            self.config['samplerate'] = int(device_info['default_samplerate'])
        if 'channels' not in self.config:
            self.config['channels'] = device_info['max_input_channels']

    def open(self):
        '''Opens Audio stream'''
        try:
            self.configure()
            self.audio = sd.InputStream(
                device=self.config['device'],
                channels=self.config['channels'],
                samplerate=self.config['samplerate']
            )
            self.audio.start()
        except Exception as e:
            log.warning(f'Failed to load audio stream: {exc}')
        self.log_start()

    def read(self):
        '''Reads in audio blocks'''
        audio = None

        if self.audio:
            audio, overflow = self.audio.read(self.config['blocksize'])
            if overflow:
                audio = None
                log.warning('Audio block overflow')

        return audio, timestamp_now()

    def close(self):
        if self.audio:
            self.audio.close()
        self.audio = None

# Fallback for no pylon
if sd is None:
    class AudioPortInput(Input):
        def __init__(self, *args, **kargs):
            Input.__init__(self)
            log.error("SoundDevice not found")
