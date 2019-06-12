"""
Script that contains code to read audio from a stream


Author: Jacob Schofield (jacob.schofield@senseye.co) - May 2019
"""
# Standard imports
import logging
import numpy as np
try:
    import soundfile as sf
except:
    sf = None
# Custom imports
from senseye_utils import LoopThread
from . audio.webcam_audio import WebcamAudio
log = logging.getLogger(__name__)


class AudioRecorder(LoopThread):
    """
    Records audio from an input source to a file
    """

    def __init__(self, audio_path=None, audio_type='webcam', audio_config={}, audio_id=0):
        """
        Initializes audio recorder

        Args:
            audio_path (str): Full audio path/filename to save to
            audio_type (str): Audio type (for now webcam, idk if this will change, I don't love the name)
            audio_config (dict): Configuration for the audio stream
            audio_id (int): Audio source ID
        """
        # Initialize
        LoopThread.__init__(self, frequency=440)

        self.audio = WebcamAudio(config=audio_config, id=audio_id)
        self.audio_type = audio_type
        self.audio_id = audio_id
        self.path = audio_path
        self.audio_data = np.empty([0, self.audio.config['channels']])

    def set_path(self, path=None):
        self.path = path

    def write(self):
        """
        Write output data to a file
        """
        log.info(f'Writing audio file to {self.path}')
        if self.audio_data.shape[0] == 0:
            log.warning('No audio recorded, not writing file')
        else:
            with sf.SoundFile(self.path, mode='w', samplerate=self.audio.config['samplerate'],
                              channels=self.audio.config['channels'], subtype=self.audio.config['subtype']) as file:
                file.write(self.audio_data)

    def on_start(self):
        """
        Opens the audio and initializes RapidEvents.
        """
        self.audio.open()

    def loop(self):
        """
        Reads audio blocks.
        """
        block, timestamp = self.audio.read()
        if block is not None:
            self.audio_data = np.vstack([self.audio_data, block])
        else:
            log.warning('WARNING! Audio block was dropped')

    def on_stop(self):
        """
        Writes audio data to a file and closes out the stream
        """
        # Write data
        if self.audio:
            self.write()
        # Close audio
        if self.audio:
            self.audio.close()
            self.audio = None

        log.info(f'audio {self.audio_type}:{self.audio_id} closing.')

if sf is None:
    class AudioRecorder(LoopThread):
        def __init__(self, *args, **kwargs):
            LoopThread.__init__(self, frequency=1)
            log.error("sndfile library not found.")

        def loop(self):
            pass
