import cv2
import config
import time

import network as networktables
from cameras import logitech_c270, generic
from processing import cube_tracker
from controls import main_controller
from controls import CAMERA_MODE_RAW, CAMERA_MODE_BALL, CAMERA_MODE_HEXAGON

def main():

    networktables.init()

    dashboard = networktables.get()

    dashboard.putBoolean(networktables.keys.vision_initialized, True)

    main_controller.connect()

    cap = None
    while(True):

        if main_controller.enable_camera:

            if cap is None:
                cap = cv2.VideoCapture(config.video_source_number)

            _, frame = cap.read()

            if main_controller.camera_mode == CAMERA_MODE_RAW:

                frame = cube_tracker.process(frame, logitech_c270)

            cv2.imshow('frame', frame )

        else:
            # IDLE mode
            cv2.destroyAllWindows()
            time.sleep(.3)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    if cap is not None:
        cap.release()



def single_frame(debug=False):

    img = cv2.imread("frc_cube.jpg")
    img = cube_tracker.process(img,
                               generic)

    cv2.imshow('Objects Detected',img)
    cv2.waitKey()

if __name__ == '__main__':
    main()