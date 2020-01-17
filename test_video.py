import cv2
import config
import time

from multiprocessing import Process

from processing import colors
import network as networktables
from cameras import logitech_c270, generic
from profiles import color_profiles
from processing import bay_tracker
from processing import port_tracker
from processing import ball_tracker
from controls import main_controller


from processing import filters

from controls import CAMERA_MODE_RAW, CAMERA_MODE_LOADING_BAY, CAMERA_MODE_BALL, CAMERA_MODE_HEXAGON
import gst_utils

import logging

import start_web
from websocket import create_connection
import json
from cameras import Camera

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

    main_controller.connect()

    cap = cv2.VideoCapture('media/yellow_ball.mp4')

    # out_pipeline = gst_utils.get_udp_streamer_pipeline2(config.gstreamer_client_ip,
    #                                          config.gstreamer_client_port,
    #                                          config.gstreamer_bitrate)

    out_pipeline = gst_utils.get_udp_sender(config.gstreamer_client_ip,
                                            config.gstreamer_client_port)


    # Set camera properties
    camera = Camera(cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                    cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                    cap.get(cv2.CAP_PROP_FPS))

    print([camera.FRAME_WIDTH])
    print([camera.FRAME_HEIGHT])
    print([camera.FPS])

    out = cv2.VideoWriter(out_pipeline, 0,
                          camera.FPS,
                          (camera.FRAME_WIDTH, camera.FRAME_HEIGHT),
                          True)

    #TODO: if no camera, exit and msg no camera
    time.sleep(5)
    logger.info('starting main loop')
    ws = create_connection("ws://localhost:8080/tracking/ws")

    frame_cnt = 0
    while(True):

        frame_cnt += 1

        if True or main_controller.enable_camera:

            if not cap.isOpened():
                print('opening camera')
                cap.open(config.video_source_number)

            _, frame = cap.read()

            if frame is None:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                frame_cnt = 0
                continue

            #frame = filters.resize(frame, camera.FRAME_WIDTH, camera.FRAME_HEIGHT)

            if main_controller.camera_mode == CAMERA_MODE_RAW:

                frame = frame

            elif main_controller.camera_mode == CAMERA_MODE_LOADING_BAY:

                frame = bay_tracker.process(frame,
                                            generic,
                                            color_profiles.ReflectiveProfile())

            elif main_controller.camera_mode == CAMERA_MODE_BALL:

                frame, tracking_data = ball_tracker.process(frame,
                                                            camera,
                                                            frame_cnt)

                ws.send(json.dumps(dict(targets=tracking_data)))

            elif main_controller.camera_mode == CAMERA_MODE_HEXAGON:

                frame = port_tracker.process(frame, generic, color_profiles.ReflectiveProfile())


            if main_controller.enable_streaming:
                # always output to 640x480

                cv2.putText(frame,
                            'Tracking Mode %s' % main_controller.camera_mode,
                            (10,10),
                            cv2.FONT_HERSHEY_DUPLEX,
                            .4,
                            colors.BLUE,
                            1,
                            cv2.LINE_AA)


                #out.write(frame)

            #cv2.imshow('frame', frame )
            #v2.waitKey(1)

        else:
            # IDLE mode
            #if cap.isOpened():
                #print('closing camera')
                #cap.release()
            time.sleep(.3)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break





def single_frame(debug=False):

    img = cv2.imread("frc_cube.jpg")
    img = cube_tracker.process(img,
                               generic)

    cv2.imshow('Objects Detected',img)
    cv2.waitKey()

if __name__ == '__main__':
    p = Process(target=start_web.main)
    p.start()
    main()
    p.join()
