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
from processing import ball_tracker2
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

from cameras import Camera
from web.handlers import main_controller


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

    cv2.destroyAllWindows()

    networktables.init(client=False)

    dashboard = networktables.get()
    dashboard.putBoolean(networktables.keys.vision_initialized, True)

    cv2.destroyAllWindows()

    cap = cv2.VideoCapture(config.video_source_number)

    # out_pipeline = gst_utils.get_udp_streamer_pipeline2(config.gstreamer_client_ip,
    #                                          config.gstreamer_client_port,
    #                                          config.gstreamer_bitrate)

    # out_pipeline = gst_utils.get_udp_sender(config.gstreamer_client_ip,
    #                                        config.gstreamer_client_port)

    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 120)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    cap.set(cv2.CAP_PROP_EXPOSURE, 0.02)
    cap.set(cv2.CAP_PROP_CONTRAST, 0.0)

    # Set camera properties
    camera = Camera(cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                    cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                    cap.get(cv2.CAP_PROP_FPS))


    # print([camera.FRAME_WIDTH])
    # print([camera.FRAME_HEIGHT])
    # print([camera.FPS])

    # out = cv2.VideoWriter(out_pipeline, 0,
    #                      camera.FPS,
    #                      (camera.FRAME_WIDTH, camera.FRAME_HEIGHT),
    #                      True)

    #TODO: if no camera, exit and msg no camera
    # time.sleep(1)


    #websocket.enableTrace(True)

    def update_controls(ws, message):
        logger.info(message)

    def ws_closed(ws):
        logger.info('closed socket')

    def on_error(ws, error):
        print(error)

    # tracking_ws = create_connection("wss://localhost:8080/tracking/ws/")
    #

    def on_open(ws):
        def run(*args):
            for i in range(3):
                time.sleep(1)
                ws.send("Hello %d" % i)
            time.sleep(1)
            ws.close()
            print("thread terminating...")
        thread.start_new_thread(run, ())

    tracking_ws = create_connection("ws://localhost:8080/tracking/ws")

    def start_dashboard_socket(*args):
        dashboard_ws = websocket.WebSocketApp("ws://localhost:8080/dashboard/ws",
            on_message = update_controls,
            on_close= ws_closed,
            on_error = on_error)
        dashboard.on_open = on_open
        dashboard_ws.run_forever()

    thread.start_new_thread(start_dashboard_socket, ())

    logger.info('starting main loop ')
    frame_cnt = 0
    while(True):

        frame_cnt += 1

        if True or main_controller.enable_camera:

            if not cap.isOpened():
                print('opening camera')
                cap.open(config.video_source_number)

            _, frame = cap.read()
            #frame = filters.resize(frame, camera.FRAME_WIDTH, camera.FRAME_HEIGHT)
            if main_controller.camera_mode == CAMERA_MODE_RAW:

                frame = frame

            elif main_controller.camera_mode == CAMERA_MODE_LOADING_BAY:
            
                frame, tracking_data = bay_tracker.process(frame, generic)
                dashboard.putStringArray(networktables.keys.vision_target_data, tracking_data)
                tracking_ws.send(json.dumps(dict(targets=tracking_data)))

            elif main_controller.camera_mode == CAMERA_MODE_BALL:

                frame, tracking_data = ball_tracker2.process(frame, generic, frame_cnt)
                dashboard.putStringArray(networktables.keys.vision_target_data, tracking_data)
                tracking_ws.send(json.dumps(dict(targets=tracking_data)))

            elif main_controller.camera_mode == CAMERA_MODE_HEXAGON:

                frame, tracking_data = port_tracker.process(frame, generic)
                dashboard.putStringArray(networktables.keys.vision_target_data, tracking_data)
                tracking_ws.send(json.dumps(dict(targets=tracking_data)))

            # logger.info(main_controller.camera_mode)
            if main_controller.enable_streaming:
                cv2.putText(frame,
                            'Tracking Mode %s' % main_controller.camera_mode,
                            (10,10),
                            cv2.FONT_HERSHEY_DUPLEX,
                            .4,
                            colors.BLUE,
                            1,
                            cv2.LINE_AA)


                # out.write(frame)

            cv2.imshow('frame', frame )
            #cv2.waitKey(1)

        else:
            # IDLE mode
            if cap.isOpened():
                print('closing camera')
                cap.release()
            time.sleep(.3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break





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