import cv2
import config
import time

from cameras.camera import USBCam, Camera

from cameras import logitech_c270, generic
from profiles import color_profiles


from processing import filters


import logging

import json

# initiate the top level logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('app')

def main():

    # mainCam = USBCam()
    # mainCam.open(config.video_source_number)
    #
    # cap = mainCam.getCam()

    cap = cv2.VideoCapture(0)
    print(cap.isOpened())

    status = 'NOT DETECTED'
    while(True):
        #
        # if cap.isOpened():
        #     status = 'READY'
        # else:
        #     status = 'NOT DETECTED'
        #
        # if status == 'NOT DETECTED':
        #     print('opening camera')
        cap = cv2.VideoCapture(0)



        is_enabled, frame = cap.read()
        print( is_enabled)
        if frame is None:
            print('waiting for camera')
            time.sleep(1)
            continue


        cv2.imshow('frame', frame )
        cv2.waitKey(1)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break


if __name__ == '__main__':
    main()
