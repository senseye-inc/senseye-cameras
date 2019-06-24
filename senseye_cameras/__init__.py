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
from . input.input_factory import create_input
from . output.output_factory import create_output

from . input.camera_pylon import CameraPylon
from . input.camera_raw_video import CameraRawVideo
from . input.camera_usb import CameraUsb
from . input.audio_ffmpeg_input import AudioFfmpegInput
from . input.audio_port_input import AudioPortInput

from . output.video_raw import VideoRaw
from . output.video_ffmpeg import VideoFfmpeg
from . output.video_ffmpeg_bayer import VideoFfmpegBayer
from . output.audio_port_output import AudioPortOutput

from . camera_handler import CameraHandler
from . camera_reader import CameraReader
from . camera_writer import CameraWriter
from . camera_viewer import CameraViewer

from . stream import Stream
