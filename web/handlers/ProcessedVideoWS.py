from os.path import abspath, dirname, join

import uuid
from tornado.websocket import WebSocketHandler, WebSocketClosedError
import logging

logger = logging.getLogger(__name__)

class ProcessedVideoWS(WebSocketHandler):
    """
    """
    watchers = set()
    def open(self):
        self.uid = str(uuid.uuid4())
        logger.info("ProcessedVideoWS websocket opened %s" % self.uid)
        ProcessedVideoWS.watchers.add(self)

    def check_origin(self, origin):
        """
            Allow CORS requests
        """
        return True

    """
    broadcast to clients, assumes its target data
    """
    def on_message(self, message):
        # logger.info('pushing image')
        for waiter in ProcessedVideoWS.watchers:
            if waiter == self:
                continue
            waiter.write_message(message, binary=True)

    def send_msg(self, msg):
        try:
            self.write_message(msg, False)
        except WebSocketClosedError:
            logger.warn("websocket closed when sending message")

    def on_close(self):
        logger.info("ProcessedVideoWS websocket closed %s" % self.uid)
        ProcessedVideoWS.watchers.remove(self)
