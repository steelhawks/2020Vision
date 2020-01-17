import tornado.web
from tornado.ioloop import IOLoop
from os.path import abspath, dirname, exists, join
import config
import logging

from tornado.web import StaticFileHandler
from web.handlers import NonCachingStaticFileHandler, DashboardWebSocket, ObjectTrackingWebSocket

logger = logging.getLogger("tornado")

def start():

    # setup tornado application with static handler + networktables support
    www_dir = abspath(join(dirname(__file__), "www"))
    lib_dir = abspath(join(dirname(__file__), "www", "lib"))

    index_html = join(www_dir, "index.html")

    app = tornado.web.Application([
        ("/dashboard/ws", DashboardWebSocket),
        ("/tracking/ws", ObjectTrackingWebSocket),
        (r"/()", NonCachingStaticFileHandler, {"path": index_html}),
        (r'/lib/(.*)', StaticFileHandler, {"path": lib_dir}),
        (r"/(.*)", NonCachingStaticFileHandler, {"path": www_dir})
    ])

    # Start the app
    logger.info("Listening on http://localhost:%s/", config.tornado_server_port)

    app.listen(config.tornado_server_port)
    IOLoop.current().start()
