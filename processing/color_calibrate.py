"""

Object Tracker based on a color profile

uses contour lines and rough area calculations

"""

import cv2
from processing import colors
from processing import cvfilters

def process(img,
            camera,
            profile):

    FRAME_WIDTH = camera.FRAME_WIDTH
    FRAME_HEIGHT = camera.FRAME_HEIGHT
    #
    # original_img = img
    #
    # img = cvfilters.resize(img, camera.FRAME_WIDTH, camera.FRAME_HEIGHT )

    rgb_mask = cvfilters.rgb_threshold(img, profile)
    #
    img = cvfilters.apply_mask(img, rgb_mask)
    #
    # img = cvfilters.hsv_threshold(img, profile)
    #

    return img


