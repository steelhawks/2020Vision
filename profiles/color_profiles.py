"""
OpenCV Constants for filters

"""
from profiles import color_profile

BALL_COLOR_PROFILE = color_profile.ColorProfile("BALL")

BALL_COLOR_PROFILE.hsv_hue.min = 50
BALL_COLOR_PROFILE.hsv_hue.max = 255
BALL_COLOR_PROFILE.hsv_sat.min = 0
BALL_COLOR_PROFILE.hsv_sat.max = 255
BALL_COLOR_PROFILE.hsv_val.min = 50
BALL_COLOR_PROFILE.hsv_val.max = 205

PORT_COLOR_PROFILE = color_profile.ColorProfile("PORT")

PORT_COLOR_PROFILE.hsv_hue.min = 10
PORT_COLOR_PROFILE.hsv_hue.max = 30
PORT_COLOR_PROFILE.hsv_sat.min = 124
PORT_COLOR_PROFILE.hsv_sat.max = 255
PORT_COLOR_PROFILE.hsv_val.min = 138
PORT_COLOR_PROFILE.hsv_val.max = 255

BAY_COLOR_PROFILE = color_profile.ColorProfile('BAY')

BAY_COLOR_PROFILE.hsv_hue.min = 0
BAY_COLOR_PROFILE.hsv_hue.max = 164
BAY_COLOR_PROFILE.hsv_sat.min = 86
BAY_COLOR_PROFILE.hsv_sat.max = 255
BAY_COLOR_PROFILE.hsv_val.min = 197
BAY_COLOR_PROFILE.hsv_val.max = 255

