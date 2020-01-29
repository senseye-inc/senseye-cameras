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
import time
from senseye_cameras import create_input, create_output

# create and open various types of cameras
pylon_cam = create_input(type='pylon', config={'pfs': '/path/to/pfs.pfs'}, id=0)
pylon_cam.open()
frame, timestamp = pylon_cam.read()
pylon_cam.close()

usb_cam = create_input(type='usb', id=0)
usb_cam.open()
frame, timestamp = usb_cam.read()
usb_cam.close()

# almost all classes/methods have extensive documentation that can be accessed via the 'help' function

# show docs that lists supported input types
help(create_input)

# show docs that lists supported output types
help(create_output)

# camera docuemntation
help(pylon_cam)
help(usb_cam)

# a Stream is a higher-level class that links an input/output.
from senseye_cameras import Stream

# Stream kwarg docs
help(Stream)

# this stream opens a usb camera and writes encoded frames to 'video.avi'
s = Stream(
    input_type='usb',
    output_type='ffmpeg', config={'fps': 30}, path='./video.avi',
)
s.start()

s.start_reading()
time.sleep(2)

s.start_writing()
time.sleep(2)

s.stop_writing()
time.sleep(1)

s.stop()

def on_frame_read(data, timestamp):
    print(data)

frames_written = 0
def on_frame_write(data):
    global frames_written
    frames_written += 1

# this stream opens a pylon camera and writes raw frames to 'raw.raw'
# this stream reads/writes automatically on start
# this stream prints out all frames read, and increments a counter on frame written
s = Stream(
    input_type='pylon',
    output_type='raw', path='./raw.raw',
    reading=True, writing=True,
    on_read=on_frame_read, on_write=on_frame_write,
)
s.start()
time.sleep(2)

s.stop()

print(frames_written)
```
