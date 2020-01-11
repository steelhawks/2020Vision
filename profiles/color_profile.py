
class Range:

    def __init__(self, min, max):
        self.min = min
        self.max = max


class ColorProfile:

    def __init__(self):

        self.red = Range(0,255)
        self.green = Range(0,255)
        self.blue = Range(0,255)

        self.hsl_hue = Range(0,255)
        self.hsl_sat = Range(0,255)
        self.hsl_lum = Range(0,255)

        self.hsv_hue = Range(0,255)
        self.hsv_sat = Range(0,255)
        self.hsv_val = Range(0,255)
