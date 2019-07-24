import logging
import atexit

from senseye_utils.date_utils import timestamp_now

log = logging.getLogger(__name__)


class Input:
    '''General interface for cameras/other frame sources.'''

    def __init__(self, id=0, config={}, defaults={}):
        self.id = id
        self.input = None
        self.config = {**defaults, **config}
        atexit.register(self.close)


    def open(self):
        '''Initializes the camera.'''
        log.warning(f'Open not implemented for {str(self)}.')

    def read(self):
        log.warning(f'Read not implemented for {str(self)}.')
        return None, timestamp_now()

    def close(self):
        '''Properly disposes of the camera object.'''
        log.warning(f'Close not implemented for {str(self)}.')

    def __str__(self):
        return f'{self.__class__.__name__}:{self.id}'
