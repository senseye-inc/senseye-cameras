from setuptools import setup

# Get version number from version file
with open('.version', 'r') as f:
    VERSION = f.read()

PYEMERGENT_VERSION='0.1.4'
SENSEYE_UTILS_VERSION='0.9.5'

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
        f'pyemergent >= {PYEMERGENT_VERSION}; platform_system=="Windows"',
        'pypylon; platform_system=="Windows"',

        'sounddevice',
        'soundfile',

        'numpy',
        'opencv-python',

        f'senseye_utils @ git+ssh://git@bitbucket.org/senseyeinc/senseye_utils@v{SENSEYE_UTILS_VERSION}'
    ],
)
