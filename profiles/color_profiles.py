"""
OpenCV Constants for filters

"""


class ReflectiveProfile:
    # RGB thresholds
    red = [95, 255]
    green = [158, 255.0]
    blue = [150, 255]

    # HSL thresholds
    hsl_hue = [22.66187050359712, 180.0]
    hsl_sat = [48.1564748201439, 255.0]
    hsl_lum = [61.915467625899275, 255.0]

    # HSV thresholds
    # hsv_hue = [0, 38]
    # hsv_sat = [78,255]
    # hsv_val = [64,255]
    
    hsv_hue = [0, 180]
    hsv_sat = [0, 255]
    hsv_val = [250, 255]


class BallProfile:

    """
    * 2020 Ballprofile Settings
    * Due to limelight coloration one issue may be configuring the rgb and hsv values...
    * Hali and Nick :)
    """

    # red = [86, 255]
    # green = [120, 255]
    # blue = [0, 100]
    red = [94, 255]
    green = [120, 255]
    blue = [23, 255]

    # HSL thresholds
    hsl_hue = [22.66187050359712, 180.0]
    hsl_sat = [48.1564748201439, 255.0]
    hsl_lum = [61.915467625899275, 255.0]

    # HSV thresholds
    # hsv_hue = [0, 38]
    # hsv_sat = [78,255]
    # hsv_val = [64,255]
    # hsv_hue = [20, 60]
    # hsv_sat = [70, 255]
    # hsv_val = [40, 255]
    hsv_hue = [20, 62]
    hsv_sat = [66, 186]
    hsv_val = [107, 255]
    
