import logging
from senseye_utils import LoopThread, SafeQueue

from . output.output_factory import create_output
from . input.input_factory import create_input

log = logging.getLogger(__name__)


class Reader(LoopThread):
    '''Reads data into a queue.'''
    def __init__(self, q, on_read=None, type='usb', config={}, id=0):
        LoopThread.__init__(self, frequency=200)
        self.q = q
        self.on_read = on_read

        self.type = type

        self.input = create_input(type=type, config=config, id=id)
        self.input.open()

    def loop(self):
        data, timestamp = self.input.read()
        if data is not None:
            if self.on_read is not None:
                self.on_read(data=data, timestamp=timestamp)
            self.q.put_nowait(data)

    def on_stop(self):
        self.input.close()


class Writer(LoopThread):
    '''Writes data from a queue into an output file.'''
    def __init__(self, q, on_write=None, type='ffmpeg', config={}, path=0):
        LoopThread.__init__(self, frequency=200)

        self.q = q
        self.on_write = on_write
        self.output = create_output(type=type, config=config, path=path)

    def loop(self):
        data = self.q.get_nowait()
        if data is not None:
            self.output.write(data)
            if self.on_write is not None:
                self.on_write(data=data)

    def set_path(self, path=None):
        self.output.set_path(path)

    def on_stop(self):
        # clear out the current q
        purge = self.q.to_list()
        for data in purge:
            self.output.write(data)
        self.output.close()


class Stream(LoopThread):
    '''
    IO Stream with a reader/writer on seperate threads.

    Args:
        input_type/input_config/id: see create_input.
        output_type/output_config/path: see create_output
        reading/writing (bool): whether to read/write on start.
        on_read (func): called on frame read. Function should take fn(data=None, timestamp=None) as args.
        on_read/on_write (func): called on frame write. Function should take fn(data=None)
    '''

    def __init__(self,
        input_type='usb', input_config={}, id=0,
        output_type='ffmpeg', output_config={}, path=None,
        reading=False, writing=False,
        on_read=None, on_write=None,
    ):
        LoopThread.__init__(self, frequency=1)

        self.q = SafeQueue(200)

        self.input_type = input_type
        self.input_config = input_config
        self.id = id

        self.output_type = output_type
        self.output_config = output_config
        self.path = path

        self.reading = reading
        self.writing = writing

        self.on_read = on_read
        self.on_write = on_write

        self.writer = self.reader = None

    def set_path(self, path=None):
        self.path = path
        if self.writer:
            self.writer.set_path(path)

    ####################
    # READER FUNCTIONS
    ####################
    def start_reading(self):
        self.reading = True
        if self.reader is None:
            self.reader = Reader(self.q, on_read=self.on_read, type=self.input_type, config=self.input_config, id=self.id)
        self.reader.start()

    def stop_reading(self):
        if self.reader:
            self.reader.stop()
        self.reader = None
        self.reading = False

    def refresh_q(self):
        '''Purges the reader queue.'''
        with self.q.mutex:
            self.q.queue.clear()

    ####################
    # WRITER FUNCTIONS
    ####################
    def start_writing(self):
        self.writing = True
        if self.writer is None:
            self.writer = Writer(self.q, on_write=self.on_write, type=self.output_type, config=self.output_config, path=self.path)

        self.refresh_q()

        self.writer.start()

    def stop_writing(self):
        if self.writer:
            self.writer.stop()
        self.writer = None
        self.writing = False

    ####################
    # LOOPTHREAD FUNCTIONS
    ####################
    def on_stop(self):
        if self.reading:
            self.stop_reading()
        if self.writing:
            self.stop_writing()

    def on_start(self):
        if self.reading:
            self.start_reading()
        if self.writing:
            self.start_writing()

    def loop(self):
        pass
