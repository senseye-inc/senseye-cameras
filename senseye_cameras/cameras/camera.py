import os
import json
import logging
from pathlib import Path

from senseye_utils.date_utils import timestamp_now

log = logging.getLogger(__name__)


class Camera:
    '''
    General interface for cameras/other frame sources.
    '''

    def __init__(self, id=0, config={}):
        self.id = id
        self.config = config

    def open(self):
        '''
        Initializes the camera.
        '''
        log.warning("Open not implemented.")

    def read(self):
        log.warning("Read not implemented.")
        return None, timestamp_now()

    def close(self):
        '''
        Properly disposes of the camera object.
        '''
        log.warning("Close not implemented.")

    def log_camera_start(self, config_write=True, config_file='camera_config.txt'):
        '''
        Logs relevant information upon record start.
        Writes config to a file.
        '''
        # write config file
        self.config_file = 'Not written.'
        if config_write:
            self.config_file = Path(config_file).absolute()
            with open(config_file, 'w') as file:
                json.dump(self.config, file, ensure_ascii=False)

        log.info(
            f'\n\n'
            f'---------- Starting {self.__class__.__name__}:{self.id} ---------\n'
            f'PID: {os.getpid()}\n'
            f'CAMERA_CONFIG: {self.config}\n'
            f'CAMERA_CONFIG_LOC: {self.config_file}\n'
            f'\n'
        )
