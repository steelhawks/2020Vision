import cv2
from PIL import Image
from io import BytesIO

class USBCam(cv2.VideoCapture):
    """TBW."""

    def __init__(self, prop_id=0):
        """TBW."""
        super().__init__(prop_id)
        #
        # self.WIDTH = self.get(cv2.CAP_PROP_FRAME_WIDTH),
        # self.HEIGHT = self.get(cv2.CAP_PROP_FRAME_HEIGHT),
        # self.FPS = self.get(cv2.CAP_PROP_FPS)

    def read(self):
        """TBW."""
        return super().read()

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
