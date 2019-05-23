#####################
# Introduction
#####################

Senseye Camera Interface.
Can read, display, and write frames from cameras.

#####################
# Tests
#####################
```python
pip install .
nosetests
```

#####################
# Using API
#####################

This package uses IPC (inter-process-communication) from senseye_utils.

```python
from senseye_cameras import CameraReader, CameraWriter, CameraViewer, CameraHandler


"""
CameraReader(camera_feed=None, camera_type='usb', camera_config={}, camera_id=0)
    camera_feed: event to be emitted on every frame read.
    camera_type: currently supports 'usb', 'video', 'raw_video', and 'pylon'.
    camera_config: currently supports keys: 'fps', 'res', and 'codec'.
    camera_id: camera identifier.

CameraWriter(camera_feed=None, path=None, recorder_type='raw', recorder_config={})
    camera_feed: event we listen to for frames.
    path: where to write video.
    recorder_type: currently supports 'raw', 'ffmpeg', 'ffmpeg_bayer'
    recorder_config: currently supports keys: 'res', 'fps'

CameraViewer(camera_feed=None)
    camera_feed: event we listen to for frames.

CameraHandler(camera_feed=None, viewer=False,
    camera_type='usb', camera_config={}, camera_id=0,
    recorder_type='raw', recorder_config={}, path=None,
    process_manager=None)
    viewer: whether to open a camera_viewer or not
"""

# individually connecting CameraReader and CameraWriter
# NOTE: CameraViewer imshows using an opencv window, which must run on the main thread/a seperate process
cr = CameraReader(camera_feed='usb0', camera_type='usb', camera_config={'fps': 60}, camera_id=0)
cw = CameraWriter(camera_feed='usb0', path='./usb_video.avi', recorder_type='ffmpeg', recorder_config={'fps': 60})
cr.start()
cw.start()
time.sleep(5)

# connecting CameraReader, CameraWriter, CameraViewer using senseye_utils ProcessManager
from senseye_utils import ProcessManager
pm = ProcessManager()

pm.add_process(CameraReader, camera_feed='usb0', camera_id=0)
pm.add_process(CameraWriter, camera_feed='usb0', path='./usb_video.avi')
pm.add_process(CameraViewer, camera_feed='usb0')

# adding additional cameras is easy
pm.add_process(CameraReader, camera_feed='usb1', camera_id=1)
pm.add_process(CameraViewer, camera_feed='usb1')

pm.start()
time.sleep(5)
pm.stop()

# using CameraHandler, which automagically does the above for you
# CameraHandler will automatically generate a camera_feed string if you do not provide one
ch = CameraHandler(camera_type='usb', camera_id=0, path='./usb_video.avi', viewer=True)
```
