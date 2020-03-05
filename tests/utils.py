import shutil
from pathlib import Path

TMP_DIR = str(Path(Path(__file__).parent, './tmp').absolute())

SAMPLE_RAW_VIDEO = str(Path(Path(__file__).parent, './resources/test.raw').absolute())

SAMPLE_VIDEO = str(Path(Path(__file__).parent, './resources/test.mp4').absolute())

def get_tmp_file(extension='.mkv'):
    '''Get testing tmp file.'''
    return str(Path(TMP_DIR, f'tmp{extension}'))

def rm_tmp_dir():
    '''Remove testing tmp dir.'''
    shutil.rmtree(TMP_DIR)
