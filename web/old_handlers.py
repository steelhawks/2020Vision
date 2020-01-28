from os.path import abspath, dirname, join

import uuid
import logging
import time
import json
import json as json_encode

from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler
from tornado.websocket import WebSocketHandler, WebSocketClosedError

import network as networktables
from controls import main_controller
from profiles.color_profile import ColorProfileEncoder
from .nt_serial import NTSerial

root_path = abspath(join(dirname(__file__),"../"))

logger = logging.getLogger("handlers")
