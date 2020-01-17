from os.path import abspath, dirname, join

import json
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError

import logging
import time

import uuid
import network as networktables

from controls import main_controller
from .nt_serial import NTSerial

logger = logging.getLogger("handlers")

import ujson as json

class ObjectTrackingWebSocket(WebSocketHandler):
    """
    """
    watchers = set()
    def open(self):
        logger.info("ObjectTracking websocket opened")
        ObjectTrackingWebSocket.watchers.add(self)

    def check_origin(self, origin):
        """
            Allow CORS requests
        """
        return True

    """
    broadcast to clients, assumes its target data
    """
    def on_message(self, message):
        for waiter in ObjectTrackingWebSocket.watchers:
            if waiter == self:
                continue
            waiter.write_message(message)

    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("websocket closed when sending message")

    def on_close(self):
        logger.info("ObjectTracking websocket closed")
        ObjectTrackingWebSocket.watchers.remove(self)



class DashboardWebSocket(WebSocketHandler):
    """
           A tornado web handler that forwards values between NetworkTables
           and a webpage via a websocket
       """

    watchers = set()
    def open(self):
        self.uid = str(uuid.uuid4())
        logger.info("Dashboard websocket opened")

        DashboardWebSocket.watchers.add(self)

        self.ioloop = IOLoop.current()

        dashboard = networktables.get()

        ### add listener network tables updates and send back to socket
        self.ntserial = NTSerial(self.send_msg_threadsafe)
        self.write_message(self.uid)
        self.write_message(dashboard.getValue(networktables.keys.vision_color_profile,{}))

    def check_origin(self, origin):
        """
            Allow CORS requests
        """
        return True

    def on_message(self, message):
        dashboard = networktables.get()
        logger.info(message)
        if message == 'status':
            dashboard.getValue(networktables.keys.vision_color_profile, {})
        else:
            inputs = json.loads(message)

            if 'controls' in inputs:
                controls = inputs['controls']
                dashboard.putBoolean(networktables.keys.vision_enable_camera, controls['enable_camera'])
                dashboard.putValue(networktables.keys.vision_camera_mode, controls['camera_mode'])

            elif 'color_profile' in inputs:
                profile = inputs['color_profile']
                dashboard.putValue(networktables.keys.vision_color_profile, json.dumps(profile))

            logger.info('broadcasting to %s' % len(DashboardWebSocket.watchers))
            for watcher in DashboardWebSocket.watchers:
                watcher.write_message(message)

    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("%s: websocket closed when sending message" % self.uid)

    ## this is used by NTSerial to send updates to web
    def send_msg_threadsafe(self, data):
        self.ioloop.add_callback(self.send_msg, data)

    def on_close(self):
        logger.info("Dashboard websocket closed %s" % self.uid)
        DashboardWebSocket.watchers.remove(self)


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
