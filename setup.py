from setuptools import setup

# Get version number from version file
with open('.version', 'r') as f:
    VERSION = f.read()

PYEMERGENT_VERSION='0.1.4'

setup(
    name='senseye_cameras',
    description='Senseye Camera Utilities',
    author='Senseye Inc',
    version=VERSION,
    packages=[
        'senseye_cameras',
        'senseye_cameras.input',
        'senseye_cameras.output',
    ],
    install_requires=[
        'sounddevice',
        'soundfile',

        'numpy',
        'opencv-python',
    ],
)
