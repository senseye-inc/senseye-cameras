import os
import time
import pytest
from utils import get_tmp_file, SAMPLE_VIDEO, rm_tmp_dir

from senseye_cameras import Stream


def stream_with_extension(extension):
    tmp_path = get_tmp_file(extension=extension)

    s = Stream(
        input_type='usb', id=SAMPLE_VIDEO,
        output_type='file', path=tmp_path,
        reading=True, writing=True,
    )
    time.sleep(2)

    s.stop()

    assert os.stat(tmp_path).st_size > 0
    rm_tmp_dir()


@pytest.mark.parametrize('extension', ['.avi', '.mp4', '.mkv', '.yuv', '.raw'])
def test_extensions(extension):
    stream_with_extension(extension)


def test_invalid_extension():
    with pytest.raises(Exception):
        stream_with_extension('.bad')
