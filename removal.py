from realesrgan import RealESRGANer2
import numpy as np
import logging
import time
import io
import os
from PIL import Image
import math
import cv2

def init():
    model_path = "experiments/pretrained_models/RealESRGAN_x2plus.pth"
    global upsampler
    upsampler = RealESRGANer2(
        scale=2,
        model_path=model_path,
        tile=800,
        tile_pad=10,
        pre_pad=0,
        half=False)

def run(img,outscale=None):
    try:
        output, _ = upsampler.enhance(img, outscale=outscale)
    except Exception as error:
        logging.error(error)
        # print('Maybe CUDA out of memory, set `tile` smaller')
    else:
        return output
    return None;