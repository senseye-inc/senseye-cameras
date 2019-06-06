# """
# Script to test audio functions.
#
# Author: Jacob Schofield (jacob.schofield@senseye.co) - May 2019
# """
# # Standard imports
# import unittest
# import nose.tools as nt
# from unittest.mock import MagicMock
# import os
# import numpy as np
# # Custom imports
# from senseye_cameras import AudioRecorder
#
#
# class AudioTests(unittest.TestCase):
#     """
#     Test deception database functions
#     """
#     def setUp(self):
#         """
#         Initialize tests
#         """
#         self.path = os.path.join(os.getcwd(), 'test.wav')
#
#     def tearDown(self):
#         """
#         Teardown tests
#         """
#         if os.path.exists(self.path):
#             os.remove(self.path)
#
#     def test_write(self):
#         """
#         Tests the write function
#         """
#         recorder = AudioRecorder(audio_path=self.path)
#         recorder.audio_data = np.array([[10.0]], dtype=np.float32)
#         recorder.write()
#         # Check if file exists
#         exists = os.path.exists(self.path)
#         nt.assert_true(exists)
#
#     def test_loop(self):
#         """
#         Tests the loop function
#         """
#         recorder = AudioRecorder(audio_path=self.path)
#         recorder.audio = MagicMock()
#         recorder.audio.read.return_value = (np.empty((10,1)), False)
#         # Check dummy loop return
#         recorder.loop()
#         nt.assert_equal(recorder.audio_data.shape, (10,1))
#
#     def test_on_stop(self):
#         """
#         Tests the on_stop function
#         """
#         recorder = AudioRecorder(audio_path=self.path)
#         recorder.audio = MagicMock()
#         recorder.audio.close.return_value = 'foo'
#         # Test on stop
#         recorder.on_stop()
#         nt.assert_equal(recorder.audio, None)
