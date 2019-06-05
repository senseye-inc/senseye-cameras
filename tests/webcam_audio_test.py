"""
Script to test audio functions.

Author: Jacob Schofield (jacob.schofield@senseye.co) - May 2019
"""
# Standard imports
import unittest
import nose.tools as nt
from unittest.mock import MagicMock
import mock
# Custom imports
from senseye_cameras import WebcamAudio


class AudioTests(unittest.TestCase):
    """
    Test deception database functions
    """
    def test_init(self):
        """
        Tests the init function
        """
        webcam_audio = WebcamAudio()

        nt.assert_equal(webcam_audio.config['samplerate'], 44100)
        nt.assert_equal(webcam_audio.config['codec'], 'WAV')

    @mock.patch('senseye_cameras.audio.webcam_audio.sd.query_devices')
    def test_configure(self, query_device):
        """
        Tests the configure method
        """
        query_device.return_value = {'default_samplerate': 100, 'max_input_channels': 1}
        webcam_audio = WebcamAudio()
        # Remove channels/samplerate
        del webcam_audio.config['samplerate']
        del webcam_audio.config['channels']
        # Configure
        webcam_audio.configure()

        nt.assert_equal(webcam_audio.config['samplerate'], 100)
        nt.assert_equal(webcam_audio.config['channels'], 1)

    @mock.patch('senseye_cameras.audio.webcam_audio.sd.InputStream')
    def test_open(self, mock_input_stream):
        """
        Tests the open audio method.
        Mocks out the inputStream object so its kinda a dumb test
        """
        mock_input_stream.return_value = 'foo'
        webcam_audio = WebcamAudio()
        foo = webcam_audio.open()

        nt.assert_equal(foo, 'foo')

    def test_read(self):
        """
        Tests the read audio from stream method
        """
        webcam_audio = WebcamAudio()
        # Mock out object
        webcam_audio.audio = MagicMock()
        webcam_audio.audio.read.return_value = ([10], False)
        block, time = webcam_audio.read()

        nt.assert_equal([10], block)

    def test_read_no_audio(self):
        """
        Tests the read audio from stream with no audio
        """
        webcam_audio = WebcamAudio()
        webcam_audio.audio = None
        # webcam_audio.audio.read.return_value = (None, False)
        block, time = webcam_audio.read()

        nt.assert_equal(None, block)

    def test_read_overflow(self):
        """
        Tests the read audio from stream when an overflow occurs
        """
        webcam_audio = WebcamAudio()
        webcam_audio.audio = MagicMock()
        webcam_audio.audio.read.return_value = ([10], True)
        block, time = webcam_audio.read()

        nt.assert_equal(None, block)

