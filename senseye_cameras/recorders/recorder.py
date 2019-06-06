import os
import json
import logging
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)


class Recorder:
    '''
    General interface for frame writing.
    Takes a path, config, and suffix.

    'path' points to the final destination of our video.
    Writes to a generated 'tmp_path'.
    When finished writing, renames 'tmp_path' to 'path'.
    tmp_paths allow users to change 'path' while the 'tmp_path' is being written to.
    '''

    def __init__(self, path=None, config={}, suffix=None):
        self.set_path(path=path)
        self.set_tmp_path(path=path, suffix=suffix)

        self.config = config

    def set_path(self, path=None):
        '''
        Sets up 'path' for writing.
        Makes parent directories if needed.
        '''
        self.path = Path(path).absolute()
        if self.path.exists():
            log.warning(f'{self.path} exists, overriding')
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        log.debug(f'{self.__class__.__name__} path set to {self.path}')

    def set_tmp_path(self, path, suffix=None):
        '''
        Creates a temporary file that lives in the same directory as 'path'.
        '''
        path = Path(path)
        self.tmp_path = tempfile.NamedTemporaryFile(
            prefix=path.stem,
            dir=path.parent,
            suffix=suffix,
            delete=False
        ).name
        log.debug(f'{self.__class__.__name__} tmp path set to {self.tmp_path}')

    def write(self, frame=None):
        log.warning('write not implemented.')

    def write_config(self, config_file='recorder_config.json'):
        self.config_file = Path(self.path.parent, config_file).absolute()
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file, ensure_ascii=False)
        log.info(f'Writing config to {self.config_file}')

    def close(self):
        '''
        Attempts to move the file from 'tmp_path' to 'path'.
        Writes config to path.
        '''
        try:
            Path(self.tmp_path).rename(self.path)
            log.info(f'Recording complete: {self.path}')
        except Exception as e:
            log.error(f'Recording rename failed: {e}')

        # write config file
        self.write_config()

    def log_record_start(self, ):
        '''
        Logs relevant information upon record start.
        '''
        log.info(
            f'\n\n'
            f'---------- Starting Recorder. ----------\n'
            f'name/type: {self.__class__.__name__}\n'
            f'path: {self.path}\n'
            f'tmp_path: {self.tmp_path}\n'
            f'config: {self.config}\n'
            f'----------------------------------------\n'
        )
