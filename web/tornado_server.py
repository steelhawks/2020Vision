import tornado.web
from tornado.ioloop import IOLoop
from os.path import abspath, dirname, exists, join
import config
import logging

from cameras.camera import USBCam
from tornado.web import StaticFileHandler
from web.handlers import NonCachingStaticFileHandler, DashboardWebSocket, ObjectTrackingWebSocket
from web.image_stream_handlers import ImagePushStreamHandler

from profiles.color_profile import ColorProfile
import controls

logger = logging.getLogger("tornado")

def start():

    # setup tornado application with static handler + networktables support
    www_dir = abspath(join(dirname(__file__), "www"))
    lib_dir = abspath(join(dirname(__file__), "www", "lib"))

    color_profile_map = {}
    for profile in [controls.CAMERA_MODE_RAW,
                    controls.CAMERA_MODE_BALL,
                    controls.CAMERA_MODE_HEXAGON,
                    controls.CAMERA_MODE_LOADING_BAY]:

        color_profile_map[profile] = ColorProfile(profile)

    app = tornado.web.Application(
        handlers=[
            ("/dashboard/ws", DashboardWebSocket),
            ("/tracking/ws", ObjectTrackingWebSocket),
            (r"/camera/ws", ImagePushStreamHandler),
            (r"/calibrate/()", NonCachingStaticFileHandler, {"path": join(www_dir, "camera.html")}),
            (r"/()", NonCachingStaticFileHandler, {"path": join(www_dir, "index.html")}),
            (r'/lib/(.*)', StaticFileHandler, {"path": lib_dir}),
            (r"/(.*)", NonCachingStaticFileHandler, {"path": www_dir})
        ],
        sockets=[],
        color_profiles=color_profile_map,
        camera=USBCam()
    )

    ImagePushStreamHandler.start(application=app)

    # Start the app
    logger.info("Listening on http://localhost:%s/", config.tornado_server_port)

    app.listen(config.tornado_server_port)
    IOLoop.current().start()
