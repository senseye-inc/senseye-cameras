import logging

from senseye_utils.date_utils import timestamp_now

log = logging.getLogger(__name__)


class Camera:
    '''
    General interface for cameras/other frame sources.
    Takes an id and a configuration dictionary.
    '''

    def __init__(self, id=0, config={}):
        self.id = id
        self.fps = config.get('fps', 0)
        self.res = config.get('res', (0, 0))
        self.width = self.res[0]
        self.height = self.res[1]
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
