from setuptools import setup
from pathlib import Path

readme = str(Path(Path(__file__).parent.absolute(), 'README.md'))
long_description = open(readme, encoding='utf-8').read()

setup(
    name='senseye-cameras',
    version='1.0.9',
    description='Senseye Camera Utilities',
    url='https://github.com/senseye-inc/senseye-cameras',
    author='Senseye, Inc.',
    license='BSD-3-Clause',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'senseye_cameras',
        'senseye_cameras.input',
        'senseye_cameras.output',
    ],
    install_requires=[
        'numpy>=1.14.5',
        'opencv-python-headless>=4.4.0.46',
        'ffmpeg-python>=0.2.0',
        'senseye-pyueye>=0.2.0',
    ],
    extras_require={
        'test': ['pytest'],
    },
    project_urls={
        "Download": "https://github.com/senseye-inc/senseye-cameras/releases",
        "Source Code": "https://github.com/senseye-inc/senseye-cameras",
        "Documentation": "https://senseye-cameras.readthedocs.io/en/latest/",
        "Homepage": "http://senseye.co/",
    },
)
