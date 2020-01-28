import cv2
from PIL import Image
from io import BytesIO
from controls import main_controller

class USBCam():
    """TBW."""
    def __init__(self, source=0):
        if main_controller.camera_mode == "CALIBRATE":
            print("opening")
            # self.WIDTH = self.get(cv2.CAP_PROP_FRAME_WIDTH),
            # self.HEIGHT = self.get(cv2.CAP_PROP_FRAME_HEIGHT),
            # self.FPS = self.get(cv2.CAP_PROP_FPS)
                # Set camera properties
            self.cam = cv2.VideoCapture(source)
            self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cam.set(cv2.CAP_PROP_FPS, 120)
            self.cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
            self.cam.set(cv2.CAP_PROP_EXPOSURE, 0.02)
            self.cam.set(cv2.CAP_PROP_CONTRAST, 0.0)
        


    def read(self):
        """TBW."""
        return self.cam.read()

    def read_image(self):
        """TBW."""
        ok, raw = self.read()
        return convert_raw_image(raw)


class Camera():

    def __init__(self, width, height, fps, flength=0):
        self.FRAME_WIDTH = int(width)
        self.FRAME_HEIGHT = int(height)
        self.FOCAL_LENGTH = flength
        self.FPS = int(fps)
