from senseye_utils import ProcessManager

from . camera_reader import CameraReader
from . camera_writer import CameraWriter
from . camera_viewer import CameraViewer


class CameraHandler:
    '''
    Creates a CameraWriter and CameraReader process
    Links them with the 'camera_feed' variable
    '''

    def __init__(self, camera_feed=None, viewer=False,
        camera_type='usb', camera_config={}, camera_id=0,
        recorder_type='raw', recorder_config={}, path=None,
        process_manager=None
    ):

        self.camera_feed = camera_feed
        if self.camera_feed is None:
            self.camera_feed = f'camera_reader:publish:{camera_type}:{camera_id}'

        self.pm = process_manager
        if self.pm is None:
            self.pm = ProcessManager()

        # only creates a CameraWriter if a path is given.
        if path:
            self.pm.add_process(CameraWriter, camera_feed=self.camera_feed, recorder_type=recorder_type, recorder_config=recorder_config, path=path)

        if viewer:
            self.pm.add_process(CameraViewer, camera_feed=self.camera_feed)

        self.pm.add_process(CameraReader, camera_feed=self.camera_feed, camera_type=camera_type, camera_config=camera_config, camera_id=camera_id)

    def start(self):
        self.pm.start()

    def stop(self):
        self.pm.stop()
