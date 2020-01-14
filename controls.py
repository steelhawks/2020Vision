from network import controller_listener

CAMERA_MODE_RAW = 'R'
CAMERA_MODE_BALL = 'B'
CAMERA_MODE_LOADING_BAY = 'L'
CAMERA_MODE_HEXAGON = 'H'

class Controls():

    def __init__(self):
        self.enable_camera = True
        # self.enable_processing = False
        self.camera_mode = CAMERA_MODE_LOADING_BAY
        self.enable_streaming = True
        self.enable_feed = True
        self.turn_camera_off = False


    def connect(self):
        controller_listener.connect(self)

main_controller = Controls()
