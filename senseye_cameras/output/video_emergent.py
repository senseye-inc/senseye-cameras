import logging

from senseye_utils import Events

from . output import Output

log = logging.getLogger(__name__)


class VideoEmergent:
    def __init__(self, path=None, **kwargs):
        # Output.__init__(self, path=path)
        self.output = None
        self.config = None
        self.path = None
        self.tmp_path = None

    def write(self, frame=None):
        pass

    def set_path(self, path=None):
        pass

    def set_tmp_path(self, path):
        pass

    def close(self):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}'
