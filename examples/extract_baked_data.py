'''
senseye-cameras bakes in frame_count/timestamp into raw pylon frames.
these are helper functions that show how to retrieve them.
'''
# expects a raw video created by CameraPylon, checks that the timestamps and frame numbers are sane

from pathlib import Path
import numpy as np
import cv2 as cv
from tqdm import tqdm

SRC = Path('./tmp/usb.avi')

size = (1028,1232)
f_size = SRC.stat().st_size
size_gray = (size[0]//2,size[1]//2)
n_bytes = size[0]*size[1]
n_frames=f_size//n_bytes

# Treats the first 7 bytes of the image as octets forming an int64
# Returns time as a float in seconds
def extract_timestamp(np_image):
    t = 0
    for i in range(7):
        t+=int(np_image[0][i])<<(8*i) #int cast breaks out of inferred np.uint32 limit
    return t/1e6

# reads the framenumber from the 8-11 bytes of the image as a big-endian set of octets
def extract_framenumber(np_image):
    n = 0
    for i in range(4):
        n+=np_image[0][i+7]<<(8*i)
    return n

def run():
    with open(str(SRC), "rb") as f:
        for i in tqdm(range(n_frames)):
            bytes = f.read(n_bytes)
            ## SEPARATE GRBG8 ARRAY
            im = np.frombuffer(bytes,dtype=np.uint8).reshape(size)
            # extract_timestamp(im)
            print()
            print(extract_timestamp(im))
            print(extract_framenumber(im))
            cv.imshow('',cv.resize(im[:20,:20],(800,800),interpolation=cv.INTER_NEAREST))
            cv.waitKey(100)
        cv.destroyAllWindows()

run()
