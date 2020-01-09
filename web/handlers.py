from os.path import abspath, dirname, join

import json
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError

import logging
import time

import network as networktables

from controls import main_controller

logger = logging.getLogger("handlers")

class DashboardWebSocket(WebSocketHandler):
    """
           A tornado web handler that forwards values between NetworkTables
           and a webpage via a websocket
       """

    def open(self):
        logger.info("websocket opened")
        self.ioloop = IOLoop.current()

    def check_origin(self, origin):
        """
            Allow CORS requests
        """
        return True

    def on_message(self, message):

        controls = json.loads(message)

        dashboard = networktables.get()
        dashboard.putBoolean(networktables.keys.vision_enable_camera, controls['enable_camera'])

        # print(controls['enable_camera'])
        # main_controller.enable_camera = controls['enable_camera']

        data = dict(enable_camera=main_controller.enable_camera,
            camera_mode=main_controller.camera_mode,
            enable_processing=main_controller.enable_processing)

        print(json.dumps(data))
        self.send_msg_threadsafe(json.dumps(data))

    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("websocket closed when sending message")

    def send_msg_threadsafe(self, data):
        self.ioloop.add_callback(self.send_msg, data)

    def on_close(self):
        logger.info("NetworkTables websocket closed")


class NonCachingStaticFileHandler(StaticFileHandler):
    """
        This static file handler disables caching, to allow for easy
        development of your Dashboard
    """

    # This is broken in tornado, disable it
    def check_etag_header(self):
        return False

    def set_extra_headers(self, path):
        # Disable caching
        self.set_header(
            "Cache-Control", "no-store, no-cache, must-revalidate, max-age=0"
        )
