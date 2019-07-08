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
        self.set_tmp_path(path=self.path)

        self.output = None
        self.config = {**defaults, **config}

    def set_path(self, path=None):
        '''Preps self.path by creating parent directories.'''
        self.path = Path(path).absolute()
        if self.path.exists():
            log.warning(f'{self.path} exists, overriding')
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    def set_tmp_path(self, path):
        '''Generates a tmpfile name in 'path's directory.'''
        path = Path(path)
        self.tmp_path = tempfile.NamedTemporaryFile(
            prefix=path.stem,
            dir=path.parent,
            suffix=path.suffix,
            delete=True
        ).name
        log.debug(f'{str(self)} tmp path set to {self.tmp_path}')

    def write(self, data=None):
        log.warning('write not implemented.')

    def close(self):
        '''
        Attempts to move the file from 'tmp_path' to 'path'.
        Writes config to path.
        '''
        try:
            Path(self.tmp_path).replace(self.path)
        except Exception as e:
            log.error(f'Recording rename failed: {e}')

    def __str__(self):
        return f'{self.__class__.__name__}'
