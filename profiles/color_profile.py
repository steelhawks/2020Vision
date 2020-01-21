import json

class ColorProfileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ColorProfile):
            return obj.to_encodable()
        return json.JSONEncoder.default(self, obj)

class Range:

    def __init__(self, min, max):
        self.min = min
        self.max = max


class ColorProfile:

    def __init__(self, camera_mode):

        self.camera_mode = camera_mode

        self.red = Range(0,255)
        self.green = Range(0,255)
        self.blue = Range(0,255)

        self.hsl_hue = Range(0,255)
        self.hsl_sat = Range(0,255)
        self.hsl_lum = Range(0,255)

        self.hsv_hue = Range(0,255)
        self.hsv_sat = Range(0,255)
        self.hsv_val = Range(0,255)


    def to_encodable(self):
        rgb = dict(
            r=dict(min=self.red.min,
                     max=self.red.max),
            b=dict(min=self.blue.min,
                     max=self.blue.max),
            g=dict(min=self.green.min,
                     max=self.green.max)
        )

        hsl = dict(
            h=dict(min=self.hsl_hue.min,
                     max=self.hsl_hue.max),
            s=dict(min=self.hsl_sat.min,
                     max=self.hsl_sat.max),
            l=dict(min=self.hsl_lum.min,
                     max=self.hsl_lum.max)
        )

        hsv = dict(
            h=dict(min=self.hsv_hue.min,
                    max=self.hsv_hue.max),
            s=dict(min=self.hsv_sat.min,
                    max=self.hsv_sat.max),
            v=dict(min=self.hsv_hue.min,
                    max=self.hsv_hue.max)
        )

        return dict(camera_mode=self.camera_mode,
                    rgb=rgb,
                    hsv=hsv,
                    hsl=hsl)
