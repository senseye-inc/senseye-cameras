import cv2
import logging
log = logging.getLogger().getChild(__name__)

has_pylon = False
has_uvc = False
has_device = False

# Pylon and UVC only compile on Windows
try:
    from pypylon import pylon
    has_pylon = True
    log.info('Using Pylon')
except:
    pass

try:
    import uvc
    has_uvc = True
    log.info('Using UVC')
except:
    pass

# TODO: REMOVE OR ADD TO CODE BASE
try:
    import device
    has_device = True
    log.info('Using Device List')
except:
    pass


# function that gets a list of cameras
def get_camera_dict():
    """
    Returns a dictionary of cameras.
    Each device has:
        key: name of the camera.
        value: dictionary containing:
            type: type of the camera (basler, cv, pupil...).
            fullname: more descriptive/less friendly name/id of the camera.
    """
    c_dict = {}

    # windows computer
    if has_pylon:
        # get basler cameras
        baslerCameraList = pylon.TlFactory.GetInstance().EnumerateDevices()
        for camera in baslerCameraList:
            name = camera.GetModelName()
            cam_info = {}
            cam_info['type'] = 'basler'
            cam_info['fullname'] = camera.GetFullName()
            c_dict[name] = cam_info

    if has_uvc:
        # get pupil cameras
        pupilCameraList = uvc.device_list()
        for camera in pupilCameraList:
            name = camera['name']
            cam_info = {}
            cam_info['type'] = 'pupil'
            cam_info['fullname'] = camera['name']
            c_dict[name] = cam_info

    if has_device:
        # get USB cameras
        device_list = device.getDeviceList()
        if device_list:
            for index, name in enumerate(device_list):
                cam_info = {}
                cam_info['type'] = 'usb'
                cam_info['fullname'] = index
                c_dict[name] = cam_info
    else:
        # Get cameras from OpenCV
        num = 0
        while 1:
            cap = cv2.VideoCapture(num)
            if cap.isOpened():
                name = f"device {num}"
                cam_info = {}
                cam_info['type'] = 'usb'
                cam_info['fullname'] = num
                c_dict[name] = cam_info
                num += 1
            else:
                break
            cap.release()

    return c_dict
