import cv2
import config
import time

from multiprocessing import Process

from processing import colors
# import network as networktables

from cameras import logitech_c270, generic
from cameras.camera import USBCam, Camera
from cameras import image_converter

from processing import bay_tracker
from processing import port_tracker
from processing import ball_tracker2
from processing import color_calibrate


import controls
from controls import main_controller
import controller_listener

from profiles.color_profile import ColorProfile

import _thread as thread
import time

from processing import filters

from controls import CAMERA_MODE_RAW, CAMERA_MODE_LOADING_BAY, CAMERA_MODE_BALL, CAMERA_MODE_HEXAGON
import gst_utils

import logging

import start_web
import websocket
from websocket import create_connection
import ujson as json


# initiate the top level logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('app')
# creating instance of logger object(?)

def main(): # main method defined

    cv2.destroyAllWindows()

    # networktables.init(client=False)

    # dashboard = networktables.get()
    # dashboard.putBoolean(networktables.keys.vision_initialized, True)

    cv2.destroyAllWindows()

    # cap = cv2.VideoCapture(config.video_source_number)
    # cap set to a cv2 object with input from a preset source
    mainCam = USBCam()
    mainCam.open(config.video_source_number)

    if(main_controller.enable_dual_camera):
        longCam = USBCam()
        longCam.open(config.long_video_source_number)

    # Set camera properties
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # cap.set(cv2.CAP_PROP_FPS, 120)
    # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    # cap.set(cv2.CAP_PROP_EXPOSURE, 0.02)
    # cap.set(cv2.CAP_PROP_CONTRAST, 0.0)
        
    cap = mainCam.getCam()
    # Set camera properties
    camera = Camera(cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                    cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                    cap.get(cv2.CAP_PROP_FPS))

    color_profile_map = {}
    for profile in [controls.CAMERA_MODE_RAW,
                    controls.CAMERA_MODE_BALL,
                    controls.CAMERA_MODE_HEXAGON,
                    controls.CAMERA_MODE_LOADING_BAY]:

        color_profile_map[profile] = ColorProfile(profile)

    main_controller.color_profiles = color_profile_map

    time.sleep(5)

    camera_ws = create_connection("ws://localhost:8080/camera/ws")
    processed_ws = create_connection("ws://localhost:8080/processed/ws")
    calibration_ws = create_connection("ws://localhost:8080/calibration/ws")
    tracking_ws = create_connection("ws://localhost:8080/tracking/ws")
    controller_listener.start("ws://localhost:8080/dashboard/ws")

    logger.info('starting main loop ')
    frame_cnt = 0
    while(True):

        tracking_data = None

        frame_cnt += 1

        if main_controller.enable_camera:

            if not cap.isOpened():
                print('opening camera')
                if main_controller.enable_dual_camera:
                   longCam.open(config.video_source_number)                
                mainCam.open(config.wide_cam_source_number)
                # if the cap is not already open, do so
                
            if main_controller.camera_mode == CAMERA_MODE_HEXAGON and main_controller.enable_dual_camera:
                _, bgr_frame = longCam.read()
            else:
                _, bgr_frame = mainCam.read()
            
            resized_frame = cv2.resize(bgr_frame, ((int)(640), (int)(480)), 0, 0, cv2.INTER_CUBIC)
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)


            if main_controller.enable_camera_feed:

                jpg=image_converter.convert_to_jpg(rgb_frame)
                camera_ws.send_binary(jpg)
                # take rgb frame and convert it to a displayable jpg form, then send that as binary through websocket

            if main_controller.enable_calibration_feed:

                calibration_frame = rgb_frame.copy()

                calibration_frame = color_calibrate.process(calibration_frame,
                                                            camera_mode = main_controller.calibration.get('camera_mode', 'RAW'),
                                                            color_mode = main_controller.calibration.get('color_mode'),
                                                            apply_mask = main_controller.calibration.get('apply_mask', False))

                jpg=image_converter.convert_to_jpg(calibration_frame)
                calibration_ws.send_binary(jpg)


            if main_controller.camera_mode == CAMERA_MODE_RAW:

                processed_frame = rgb_frame
                # Camera mode set to "raw" - takes rgb frame

            elif main_controller.camera_mode == CAMERA_MODE_LOADING_BAY:
            
                color_profile=main_controller.color_profiles[CAMERA_MODE_LOADING_BAY]
                # Set color profile to that of "camera mode loading bay"

                processed_frame, tracking_data = bay_tracker.process(rgb_frame,
                                                            camera,
                                                            frame_cnt,
                                                            color_profile)
                                                            # Frame is displayed with bay tracking properties

            elif main_controller.camera_mode == CAMERA_MODE_BALL:

                color_profile=main_controller.color_profiles[CAMERA_MODE_BALL] # color profile set to the CAMERA MODE BALL one
                # print("ball")

                processed_frame, tracking_data = ball_tracker2.process(rgb_frame,
                                                            camera,
                                                            frame_cnt,
                                                            color_profile)

            elif main_controller.camera_mode == CAMERA_MODE_HEXAGON:

                color_profile=main_controller.color_profiles[CAMERA_MODE_HEXAGON]

                processed_frame, tracking_data = port_tracker.process(rgb_frame,
                                                            camera,
                                                            frame_cnt,
                                                            color_profile)




            if main_controller.enable_processing_feed: # once we start showing our processing feed...

                cv2.putText(processed_frame,
                            'Tracking Mode %s' % main_controller.camera_mode,
                            (10,10),
                            cv2.FONT_HERSHEY_DUPLEX,
                            .4,
                            colors.BLUE,
                            1,
                            cv2.LINE_AA)

                jpg=image_converter.convert_to_jpg(processed_frame)
                processed_ws.send_binary(jpg)

                # if out is not None:
                #     out.write(frame)
            if len(tracking_data) != 0 and main_controller.send_tracking_data:
                # sort tracking data by closests object
                logger.info(tracking_data)
                tracking_data = sorted(tracking_data, key = lambda i: i['dist'])
                tracking_ws.send(json.dumps(dict(targets=tracking_data)))
                # put into networktables
                # dashboard.putStringArray(networktables.keys.vision_target_data, tracking_data)

            # cv2.imshow('frame', processed_frame )
            # cv2.waitKey(0)

        else:
            logger.info('waiting for control socket')
            # IDLE mode
            if cap.isOpened():
                print('closing camera')
                cap.release()
            time.sleep(.3)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break



if __name__ == '__main__':
    p = Process(target=start_web.main)
    p.start()
    main()
    p.join()
