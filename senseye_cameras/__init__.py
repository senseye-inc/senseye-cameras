'''
Senseye Camera Utility Package.

abstractions:
    camera - a video/camera interface that produces frames.
    recorder - an interface that takes in frames and writes them to disk.
create a camera/recorder through the create_camera/create_recorder functions.

higher level modules:
    CameraReader: continuously reads frames. Publishes frames via ZMQ RapidEvents.
    CameraWriter: continuously writes frames. Gets frames from ZMQ RapidEvents.
    CameraViewer: continuously displays frames using opencv imshow. Gets frames from ZMQ RapidEvents.

    CameraHandler: continuously reads and writes frames.

    AudioRecorder: continuously listens to and writes audio to disk.
'''
from . cameras.camera_factory import create_camera
from . recorders.recorder_factory import create_recorder

from . cameras.pylon_camera import PylonCamera
from . cameras.raw_video_camera import RawVideoCamera
from . cameras.usb_camera import UsbCamera

from . recorders.raw_recorder import RawRecorder
from . recorders.ffmpeg_recorder import FfmpegRecorder
from . recorders.ffmpeg_bayer_recorder import FfmpegBayerRecorder
from . recorders.ffmpeg_audio import FfmpegAudio

from . camera_handler import CameraHandler
from . camera_reader import CameraReader
from . camera_writer import CameraWriter
from . camera_viewer import CameraViewer
