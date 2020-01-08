import cv2
import network as networktables

from cameras import logitech_c270, generic
from processing import cube_tracker

def main():
    networktables.init(remote=False)
    video()

def video():

    dashboard = networktables.get()

    dashboard.putBoolean(networktables.keys.vision_initialized, True)

    # cap = cv2.VideoCapture(config.video_source_number)
    #
    # while(True):
    #
    #     _, frame = cap.read()
    #
    #     img = cube_tracker.process(frame,
    #                                logitech_c270,
    #                                debug)
    #
    #     cv2.imshow('frame', frame )
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # cap.release()
    # cv2.destroyAllWindows()

def single_frame(debug=False):

    img = cv2.imread("frc_cube.jpg")
    img = cube_tracker.process(img,
                               generic,
                               debug)

    cv2.imshow('Objects Detected',img)
    cv2.waitKey()

if __name__ == '__main__':
    main()