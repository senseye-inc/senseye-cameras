"""
Script that contains the abstract class for recording audio


Author: Jacob Schofield (jacob.schofield@senseye.co) - May 2019
"""
import os
import json
import logging
from pathlib import Path

from senseye_utils.date_utils import timestamp_now

log = logging.getLogger(__name__)


class Audio:
    """
    General interface for audio.
    Takes an id and a configuration dictionary.
    """

    def __init__(self, id=0, config={}):
        self.id = id
        self.config = config

    def open(self):
        """
        Initializes the camera.
        """
        log.warning("Open not implemented.")

    def read(self):
        log.warning("Read not implemented.")
        return None, timestamp_now()

    def close(self):
        """
        Properly disposes of the camera object.
        """
        log.warning("Close not implemented.")

    def log_start(self):
        """
        Logs relevant information upon record start.
        Writes config to a file.
        """
        log.info(
            f'\n'
            f'---------- Starting {self.__class__.__name__}:{self.id} ---------\n'
            f'config: {self.config}\n'
            f'--------------------------------------'
        )
