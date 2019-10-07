import time
import atexit
import shutil
from pathlib import Path
import logging
from senseye_utils import LoopThread, SafeQueue

from . output.output_factory import create_output
from . input.input_factory import create_input

log = logging.getLogger(__name__)


class Reader(LoopThread):
    '''Reads data into a queue.'''

    def __init__(self, q, on_read=None, type='usb', config={}, id=0, frequency=None, reading=False):
        if frequency is None:
            frequency = config.get('fps', 100)
        LoopThread.__init__(self, frequency=frequency)
        self.q = q
        self.on_read = on_read

        self.type = type

        self.input = create_input(type=type, config=config, id=id)
        self.input.open()
        self.reading = reading
        log.info(f'Started {str(self.input)}. Config: {self.input.config}')

    def loop(self):
        if self.reading:
            data, timestamp = self.input.read()
            if data is not None:
                if self.on_read is not None:
                    self.on_read(data=data, timestamp=timestamp)
                self.q.put_nowait(data)

    def on_stop(self):
        self.input.close()
        log.info(f'Stopped {str(self.input)}.')


class Writer(LoopThread):
    '''Writes data from a queue into an output file.'''
    def __init__(self, q, on_write=None, type='ffmpeg', config={}, path=0, frequency=None):
        if frequency is None:
            frequency = config.get('fps', 100)
        LoopThread.__init__(self, frequency=frequency)

        self.q = q
        self.on_write = on_write
        self.output = create_output(type=type, config=config, path=path)
        log.info(f'Started {str(self.output)}. Config: {self.output.config}')

    def loop(self):
        data = self.q.get_nowait()
        if data is not None:
            self.output.write(data)
            if self.on_write is not None:
                self.on_write(data=data)

    def set_path(self, path=None):
        self.output.set_path(path)
        log.info(f'{str(self)} path set to {path}')

    def on_stop(self):
        # clear out the current q
        purge = self.q.to_list()
        for data in purge:
            self.output.write(data)
        self.output.close()
        log.info(f'Stopped {str(self.output)}. Path: {self.output.path}')

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
        output_type='ffmpeg', output_config={}, path='.',
        input_frequency=None, output_frequency=None,
        reading=False, writing=False,
        on_read=None, on_write=None,
        min_disk_space_bytes=-1,
    ):
        LoopThread.__init__(self, frequency=1)

        self.q = SafeQueue(700)

        self.min_disk_space_bytes = min_disk_space_bytes

        self.input_type = input_type
        self.input_config = input_config
        self.id = id

        self.output_type = output_type
        self.output_config = output_config
        self.path = path

        self.input_frequency = input_frequency
        self.output_frequency = output_frequency

        self.on_read = on_read
        self.on_write = on_write

        self.writer = self.reader = None
        atexit.register(self.stop)

        self.reader = Reader(self.q, on_read=self.on_read, type=self.input_type, config=self.input_config, id=self.id, frequency=self.input_frequency)
        self.reader.start()

        if reading:
            self.start_reading()
        if writing:
            self.start_writing()

    def set_path(self, path=None):
        self.path = path
        if self.writer:
            self.writer.set_path(path)

    ####################
    # READER FUNCTIONS
    ####################
    def start_reading(self):
        self.reader.reading = True

    def stop_reading(self):
        self.reader.reading = False

    def refresh_q(self):
        '''Purges the reader queue.'''
        with self.q.mutex:
            self.q.queue.clear()

    def set_prop(self, name=None, value=None):
        if self.reader and self.reader.input:
            self.reader.input.set_prop(name, value)

    def get_prop(self, name=None):
        if self.reader and self.reader.input:
            return self.reader.input.get_prop(name)
        return None

    ####################
    # WRITER FUNCTIONS
    ####################
    def start_writing(self):
        if self.min_disk_space_bytes > 0:
            total, used, free = shutil.disk_usage(str(Path(self.path).parent.absolute()))
            if free < self.min_disk_space_bytes:
                log.critical(f'Stream not writing, free bytes {free} lower than min_disk_space_bytes {self.min_disk_space_bytes}')
                return

        if self.writer is None:
            self.writer = Writer(self.q, on_write=self.on_write, type=self.output_type, config=self.output_config, path=self.path, frequency=self.output_frequency)

            if self.input_type == 'emergent':
                self.writer.output.set_emergent_object(self.reader.input.input)

            if self.path is None:
                self.path = f'./output/{int(time.time())}.avi'
                log.warning(f'Writer path not set. Setting path to: {self.path}')

            self.refresh_q()

            self.writer.start()

    def stop_writing(self):
        if self.writer:
            self.writer.stop()
            self.writer = None

    ####################
    # LOOPTHREAD FUNCTIONS
    ####################
    def on_stop(self):
        self.stop_reading()
        self.stop_writing()
