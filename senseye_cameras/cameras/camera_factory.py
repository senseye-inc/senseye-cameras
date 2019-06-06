import logging

from . usb_camera import UsbCamera
from . pylon_camera import PylonCamera
from . raw_video_camera import RawVideoCamera

log = logging.getLogger(__name__)


def create_camera(camera_type='usb', *args, **kwargs):
    '''
    Factory method for creating cameras.
    Currently supports 'usb', 'video', 'pylon', and 'raw_video' camera_types.
    '''
    if camera_type == 'usb' or camera_type == 'video':
        return UsbCamera(*args, **kwargs)
    if camera_type == 'pylon':
        return PylonCamera(*args, **kwargs)
    if camera_type == 'raw_video':
        return RawVideoCamera(*args, **kwargs)

    log.warning(f'Camera type: {camera_type} not supported.')
