import logging

from . output import Output

log = logging.getLogger(__name__)


class VideoEmergent(Output):
    def __init__(self, path=None, **kwargs):
        Output.__init__(self, path=path)

    def set_emergent_object(self, emergent):
        self.output = emergent
        self.output.set_path(self.tmp_path)
        self.output.start_writing()

    def write(self, frame=None):
        pass

    def close(self):
        if self.output:
            self.output.stop_writing()
            Output.close(self)
            self.output = None

    def __str__(self):
        return f'{self.__class__.__name__}'

    def start_writing(self):
        self.writing = True
        if self.input:
            self.input.start_writing() # allows any fps to be set

    def stop_writing(self):
        self.writing = False
        if self.output:
            self.output.stop_writing()

    def set_path(self, path):
        self.path = path
        if self.output:
            self.output.set_path(self.path)
