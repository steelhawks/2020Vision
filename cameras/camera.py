

class Camera():

    def __init__(self, width, height, fps, flength=0):
        self.FRAME_WIDTH = int(width)
        self.FRAME_HEIGHT = int(height)
        self.FOCAL_LENGTH = flength
        self.FPS = int(fps)
