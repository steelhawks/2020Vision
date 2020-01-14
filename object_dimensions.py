import math
#all in inches
#ratio is w to h

EXACT_PORT_RATIO = 39.25 / 17
EXACT_LOADING_RATIO = 7 / 11

class Ball:
    LENGTH = 7
    AREA = ((LENGTH / 2) ** 2) * math.pi
    RATIO = 1
class Bay:
    LENGTH = 7
    AREA = 77
    RATIO = 7 / 11

class Port:
    LENGTH = 39.25  # width of longest base
    AREA = 500.4375
    RATIO = 39.25 / 17
