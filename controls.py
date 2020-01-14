from network import controller_listener

CAMERA_MODE_RAW = 'RAW'
CAMERA_MODE_CALIBRATE = 'CALIBRATE'
CAMERA_MODE_BALL = 'BALL'
CAMERA_MODE_HEXAGON = 'HEXAGON'
CAMERA_MODE_LOADING_BAY = 'BAY'

class Controls():

    def __init__(self):
        self.enable_camera = True
        self.enable_processing = False
        self.enable_streaming = True
        self.camera_mode = CAMERA_MODE_CALIBRATE

        self.enable_feed = True
        self.turn_camera_off = False

    def connect(self):
        controller_listener.connect(self)

main_controller = Controls()
