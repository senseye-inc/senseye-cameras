'''
Senseye Camera Utility Package.

abstractions:
    camera - a video/camera interface that produces frames.
    recorder - an interface that takes in frames and writes them to disk.
create a camera/recorder through the create_camera/create_recorder functions.

'''
from . input.input_factory import create_input
from . output.output_factory import create_output

from . stream import Stream
