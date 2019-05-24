import os
import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)


class Recorder:
    '''
    General interface for frame writing.
    Takes an id and a configuration dictionary.
    '''

    def __init__(self, path=None, config={}):
        self.path = Path(path).absolute()
        try:
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        except: pass

        self.config = config

    def write(self, frame=None):
        log.warning('Write not implemented.')

    def close(self):
        log.warning('Close not implemented.')

    def log_record_start(self, config_write=True, config_file='recorder_config.txt'):
        '''
        Logs relevant information upon record start.
        Writes config to a file.
        '''
        self.path = Path(self.path)
        if self.path.is_file():
            log.warning(f"Overriding existing file: {self.path}")

        # write config file
        self.config_file = 'Not written.'
        if config_write:
            self.config_file = Path(self.path.parent, config_file).absolute()
            with open(config_file, 'w') as file:
                json.dump(self.config, file, ensure_ascii=False)

        log.info(
            f'\n\n'
            f'---------- {self.__class__.__name__} recording to file ---------\n'
            f'PID: {os.getpid()}\n'
            f'PATH: {self.path}\n'
            f'RECORDER_CONFIG: {self.config}\n'
            f'RECORDER_CONFIG_LOC: {self.config_file}\n'
            f'\n'
        )
