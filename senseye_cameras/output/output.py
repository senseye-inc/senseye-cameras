import json
import logging
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)


class Output:
    '''
    General interface for frame writing.
    Takes a path, config.

    'path' points to the final destination of our video.
    Writes to a generated 'tmp_path'.
    When finished writing, renames 'tmp_path' to 'path'.
    tmp_paths allow users to change 'path' while the 'tmp_path' is being written to.
    '''

    def __init__(self, path=None, config={}, defaults={}):
        self.set_path(path=path)
        self.set_tmp_path(path=path)

        self.output = None
        self.config = {**defaults, **config}

    def set_path(self, path=None):
        '''
        Sets up 'path' for writing.
        Makes parent directories if needed.
        '''
        self.path = Path(path).absolute()
        if self.path.exists():
            log.warning(f'{self.path} exists, overriding')
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        log.info(f'{self.__class__.__name__} path set to {self.path}')

    def set_tmp_path(self, path):
        '''
        Creates a temporary file that lives in the same directory as 'path'.
        '''
        path = Path(path)
        self.tmp_path = tempfile.NamedTemporaryFile(
            prefix=path.stem,
            dir=path.parent,
            suffix=path.suffix,
            delete=False
        ).name
        log.debug(f'{self.__class__.__name__} tmp path set to {self.tmp_path}')

    def write(self, frame=None):
        log.warning('write not implemented.')

    def close(self):
        '''
        Attempts to move the file from 'tmp_path' to 'path'.
        Writes config to path.
        '''
        # renames tmp_path to path
        try:
            Path(self.tmp_path).rename(self.path)
        except Exception as e:
            log.error(f'Recording rename failed: {e}')

        # writes config file
        config_file = Path(self.path.parent, f'{self.__class__.__name__}.json').absolute()
        with open(config_file, 'w') as file:
            json.dump(self.config, file, ensure_ascii=False)

        # pretty logging
        log.info(
            f'\n'
            f'---------- Stopping {self.__class__.__name__}. ----------\n'
            f'path: {self.path}\n'
            f'config: {self.config}\n'
            f'config_file: {config_file}\n'
            f'----------------------------------------'
        )

    def log_start(self):
        '''
        Logs relevant information upon record start.
        '''
        log.info(
            f'\n'
            f'---------- Starting {self.__class__.__name__}. ----------\n'
            f'tmp_path: {self.tmp_path}\n'
            f'----------------------------------------'
        )
