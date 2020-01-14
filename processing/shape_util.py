import cv2
import math
###

###
def dimensions_match(contour, vertices, desired_ratio):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    # print(len(approx))
    # if
    if len(approx) == vertices or len(approx) == vertices - 1 or len(approx) == vertices + 1:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(approx)
        # print(w)
        # print(h)
        if (desired_ratio < 1 and w > h) or (desired_ratio > 1 and h > w):
            temp = w
            w = h
            h = temp
        MIN_RATIO = desired_ratio * 0.5
        MAX_RATIO = desired_ratio * 1.50

        ar = w / float(h)
        # print(ar)
        #
        if MIN_RATIO <= ar <= MAX_RATIO:
            return True

    return False


def find_vertices(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    return len(approx)

def get_angle(camera, x, y):
    a = float(abs(camera.FRAME_WIDTH / 2 - x))
    b = float(camera.FRAME_HEIGHT - y)

    radians = math.atan(a / b)
    angle = radians * 180 / math.pi
    return angle


def get_distance(width_pixel, width_actual, focal_length):
    return focal_length * width_actual / width_pixel