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

    def write(self, frame=None):
        log.warning('Write not implemented.')

    def close(self):
        log.warning('Close not implemented.')
