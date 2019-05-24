import logging
from types import SimpleNamespace

log = logging.getLogger(__name__)


def configure(object, config={}, defaults={}):
    '''
    Sets an objects attributes given a config + defaults
    '''
    merged = {**defaults, **config}
    for k, v in merged.items():
        setattr(object, k, v)

    return merged

def ffmpeg_string(**kwargs):
    '''
    Generates an ffmpeg string given kwargs.
    '''
    # didn't want to deal with dictionary access, hence simplenamespace
    n = SimpleNamespace(**kwargs)

    ret_str = 'ffmpeg '
    # log level
    ret_str += f'-hide_banner -loglevel warning '
    # continue without user input
    ret_str += f'-y '
    # format
    if hasattr(n, 'format'):
        ret_str += f'-f {n.format} '
    # pixel format
    if hasattr(n, 'pixel_format'):
        ret_str += f'-pixel_format {n.pixel_format} '
    # resolution
    if hasattr(n, 'res'):
        ret_str += f'-s {n.res[0]}x{n.res[1]} '
    # fps
    if hasattr(n, 'fps'):
        ret_str += f'-r {n.fps} '
    # prep path
    ret_str += '-i '
    # disable audio
    ret_str += f'- -an '
    # codec
    if hasattr(n, 'codec'):
        ret_str += f'-c:v {n.codec} '
    # pixel format
    if hasattr(n, 'path'):
        ret_str += f'{n.path} '
    else:
        log.warning("Ffmpeg string must have an output path.")
        return ''

    return ret_str
