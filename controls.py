from network import controller_listener

CAMERA_MODE_RAW = 'RAW'
CAMERA_MODE_CALIBRATE = 'CALIBRATE'
CAMERA_MODE_BALL = 'BALL'
CAMERA_MODE_HEXAGON = 'HEXAGON'
CAMERA_MODE_LOADING_BAY = 'BAY'

class Controls():

    def __init__(self):
        self.enable_camera = True

        self.enable_camera_feed = True
        self.enable_calibration_feed = False
        self.enable_processing_feed = True
        self.enable_dual_camera = True
        self.send_tracking_data = True

        self.camera_mode = CAMERA_MODE_RAW
        self.enable_feed = True
        self.color_profiles = {}


        self.calibration = {}


    def connect(self):
        controller_listener.connect(self)

    def update(message):
        print(message)

main_controller = Controls()
