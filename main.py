import cv2
import config
import time

from multiprocessing import Process

from processing import colors
import network as networktables

from cameras import logitech_c270, generic
from cameras import Camera
from cameras import image_converter

from profiles import color_profiles
from processing import bay_tracker
from processing import port_tracker
from processing import ball_tracker
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


def main():

    networktables.init(client=False)

    dashboard = networktables.get()
    dashboard.putBoolean(networktables.keys.vision_initialized, True)

    cap = cv2.VideoCapture(config.video_source_number)

    enable_gstreamer_pipeline = False

    out = None
    if enable_gstreamer_pipeline:
        out_pipeline = gst_utils.get_udp_sender(config.gstreamer_client_ip, config.gstreamer_client_port)

        # out_pipeline = gst_utils.get_udp_streamer_pipeline2(config.gstreamer_client_ip,
        #                                          config.gstreamer_client_port,
        #                                          config.gstreamer_bitrate)


        out = cv2.VideoWriter(out_pipeline, 0,
                              camera.FPS,
                              (camera.FRAME_WIDTH, camera.FRAME_HEIGHT),
                              True)

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

    tracking_ws = create_connection("ws://localhost:8080/tracking/ws")
    camera_ws = create_connection("ws://localhost:8080/camera/ws")
    processed_ws = create_connection("ws://localhost:8080/processed/ws")
    calibration_ws = create_connection("ws://localhost:8080/calibration/ws")

    controller_listener.start("ws://localhost:8080/dashboard/ws")

    logger.info('starting main loop ')
    frame_cnt = 0
    while(True):

        frame_cnt += 1

        if main_controller.enable_camera:

            if not cap.isOpened():
                print('opening camera')
                cap.open(config.video_source_number)

            _, raw_frame = cap.read()

            rgb_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

            if main_controller.camera_mode == CAMERA_MODE_RAW:

                frame = frame

            # elif main_controller.camera_mode == CAMERA_MODE_LOADING_BAY:
            #
            #     frame = bay_tracker.process(frame,
            #                                 generic,
            #                                 color_profiles.ReflectiveProfile())

            elif main_controller.camera_mode == CAMERA_MODE_BALL:

                color_profile=main_controller.color_profiles[CAMERA_MODE_BALL]

                processed_frame, tracking_data = ball_tracker.process(rgb_frame,
                                                            camera,
                                                            frame_cnt,
                                                            color_profile)

                tracking_ws.send(json.dumps(dict(targets=tracking_data)))

            elif main_controller.camera_mode == CAMERA_MODE_HEXAGON:

                processed_frame = port_tracker.process(frame, generic, color_profiles.ReflectiveProfile())


            if main_controller.enable_camera_feed:

                jpg=image_converter.convert_to_jpg(rgb_frame)
                camera_ws.send_binary(jpg)

            if main_controller.enable_calibration_feed:

                calibration_frame = raw_frame.copy()

                calibration_frame = color_calibrate.process(calibration_frame,
                                                            camera_mode = main_controller.calibration.get('camera_mode', 'RAW'),
                                                            color_mode = main_controller.calibration.get('color_mode'),
                                                            apply_mask = main_controller.calibration.get('apply_mask', False))

                jpg=image_converter.convert_to_jpg(calibration_frame)
                calibration_ws.send_binary(jpg)

            if main_controller.enable_processing_feed:

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

            #cv2.imshow('frame', frame )
            #v2.waitKey(1)

        else:
            logger.info('waiting for control socket')
            # IDLE mode
            #if cap.isOpened():
                #print('closing camera')
                #cap.release()
            time.sleep(.3)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break



if __name__ == '__main__':
    p = Process(target=start_web.main)
    p.start()
    main()
    p.join()
