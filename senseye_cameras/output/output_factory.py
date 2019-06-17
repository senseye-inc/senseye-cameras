import logging

from . video_raw import VideoRaw
from . video_ffmpeg_bayer import VideoFfmpegBayer
from . video_ffmpeg import VideoFfmpeg

log = logging.getLogger(__name__)


def create_output(type='usb', *args, **kwargs):
    '''
    Factory method for creating recorders.
    Currently supports 'raw', 'ffmpeg_bayer', and 'ffmpeg' types.
    '''
    if type == 'raw':
        return VideoRaw(*args, **kwargs)
    if type == 'ffmpeg_bayer':
        return VideoFfmpegBayer(*args, **kwargs)
    if type == 'ffmpeg':
        return VideoFfmpeg(*args, **kwargs)

    log.warning(f'Output type: {type} not supported.')
