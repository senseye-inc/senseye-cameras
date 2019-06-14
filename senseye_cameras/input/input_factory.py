import logging

from . camera_usb import CameraUsb
from . camera_pylon import CameraPylon
from . camera_raw_video import CameraRawVideo

log = logging.getLogger(__name__)


def create_input(type='usb', *args, **kwargs):
    '''
    Factory method for creating media input.
    Currently supports 'usb', 'video', 'pylon', and 'raw_video' types.
    '''
    if type == 'usb' or type == 'video':
        return CameraUsb(*args, **kwargs)
    if type == 'pylon':
        return CameraPylon(*args, **kwargs)
    if type == 'raw_video':
        return CameraRawVideo(*args, **kwargs)

    log.warning(f'Input type: {type} not supported.')
