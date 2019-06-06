import logging

from . raw_recorder import RawRecorder
from . ffmpeg_bayer_recorder import FfmpegBayerRecorder
from . ffmpeg_recorder import FfmpegRecorder

log = logging.getLogger(__name__)


def create_recorder(recorder_type='usb', *args, **kwargs):
    '''
    Factory method for creating recorders.
    Currently supports 'raw', 'ffmpeg_bayer', and 'ffmpeg' recorder_types.
    '''
    if recorder_type == 'raw':
        return RawRecorder(*args, **kwargs)
    if recorder_type == 'ffmpeg_bayer':
        return FfmpegBayerRecorder(*args, **kwargs)
    if recorder_type == 'ffmpeg':
        return FfmpegRecorder(*args, **kwargs)

    log.warning(f'Recorder type: {recorder_type} not supported.')
