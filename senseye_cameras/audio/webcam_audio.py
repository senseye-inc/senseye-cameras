"""
Script that contains code to record audio from a webcam


Author: Jacob Schofield (jacob.schofield@senseye.co) - May 2019
"""
import logging
try:
    import sounddevice as sd
except:
    sd = None

from . audio import Audio
from senseye_utils.date_utils import timestamp_now

log = logging.getLogger(__name__)


class WebcamAudio(Audio):
    """
    Class to handle recording audio using the sounddevice api for portaudio
    """

    def __init__(self, id=0, config={}):
        Audio.__init__(self, id=id, config=config)

        # set up config
        self.defaults = {
                        'samplerate': 44100,
                        'codec': 'WAV',
                        'channels': 1,
                        'device': id,
                        'blocksize': 1024,
                        'downsample': 10,
                        'subtype': 'PCM_24'
                        }
        self.config = {**self.defaults, **self.config}
        self.audio = None

    def configure(self):
        """
        Configures the audio using a config.
        Supported configurations: samplerate, codec, channels, blocksize, downsample, subtype

        Fills self.config with audio attributes.
        Logs audio start.
        """
        device_info = sd.query_devices(self.config['device'], 'input')
        if 'samplerate' not in self.config:
            self.config['samplerate'] = int(device_info['default_samplerate'])
        if 'channels' not in self.config:
            self.config['channels'] = device_info['max_input_channels']

        self.log_audio_start()

    def open(self):
        """
        Opens Audio stream
        """
        # Configure
        self.configure()
        # Open camera
        try:
            log.info('started audio recording')
            log.info(f"device {self.config['device']} | channels {self.config['channels']} | samplerate {self.config['samplerate']}")
            self.audio = sd.InputStream(
                device=self.config['device'],
                channels=self.config['channels'],
                samplerate=self.config['samplerate']
            )
            self.audio.start()
        except Exception as exc:
            log.warning(f'Failed to load audio stream: {exc}')
        log.info(f'Audio status: {self.audio}')
        return self.audio

    def read(self):
        """
        Reads in audio blocks
        """
        if self.audio is None:
            return None, timestamp_now()

        # Get blocks
        block, overflow = self.audio.read(self.config['blocksize'])
        if overflow:
            log.warning('Audio block overflow')
            return None, timestamp_now()

        # Downsample
        downsamp_block = block[::self.config['downsample']]
        return downsamp_block, timestamp_now()

    def close(self):
        if self.audio:
            self.audio.close()
            self.audio = None

# Fallback for no PortAudio
if sd is None:
    class WebcamAudio(Audio):
        def __init__(self, *args, **kargs):
            Audio.__init__(self)
            log.error("PortAudio not found")
