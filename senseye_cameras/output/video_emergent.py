import logging

from senseye_utils import Events

from . output import Output

log = logging.getLogger(__name__)


class VideoEmergent(Output):
    def __init__(self, path=None, **kwargs):
        Output.__init__(self, path=path)
        self.e = Events()

        self.e.publish('emergent:set_path', path=self.tmp_path)
        self.e.publish('emergent:start_writing')

    def write(self, frame=None):
        pass
