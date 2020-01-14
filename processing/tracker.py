"""

object Tracker based on a color profile

uses contour lines and rough area calculations

"""
import math
import cv2
from processing import colors
from processing import filters
import object_dimensions
MIN_AREA = 1000


def process(img, camera, profile, object):
    global rgb_window_active, hsv_window_active
    if(object == 'bay'):
        localObj = object_dimensions.Bay()
    if(object == 'ball'):
        localObj = object_dimensions.Ball()
    if(object == 'port'):
        localObj = object_dimensions.Port()

    FRAME_WIDTH = camera.FRAME_WIDTH
    FRAME_HEIGHT = camera.FRAME_HEIGHT

    img = filters.resize(img, camera.FRAME_WIDTH, camera.FRAME_HEIGHT)

    original_img = img

    # rgb_mask = filters.rgb_threshold(img, profile)

    # img = filters.apply_mask(img, rgb_mask)

    img = filters.hsv_threshold(img, profile)

    cv2.imshow('hsv', img)

    # img = filters.median_filter(img)


    contours, hierarchy = cv2.findContours(img,
                                              cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []

    # algorithm for detecting rectangular object (loading bay)
    for (index, contour) in enumerate(contours):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        area = cv2.contourArea(approx)
        x, y, w, h = cv2.boundingRect(approx)
        # limit the number of contours to process
        #
        if area > MIN_AREA:
            contour_list.append(contour)
            center_mass_x = x + w / 2
            center_mass_y = y + h / 2
            #
            if object == 'bay':
                isShape = find_bay(localObj.RATIO, contour, contours, index, img, camera)
                if isShape:
                    cv2.rectangle(img, (x, y), (x + w, y + h), colors.GREEN, 2)
            cv2.drawContours(img, contours, index, colors.random(), 2)
            cv2.circle(img, (int(center_mass_x), int(center_mass_y)), 5, color, -1)
            cv2.line(img, (FRAME_WIDTH // 2, FRAME_HEIGHT), (int(center_mass_x), int(center_mass_y)), color, 2)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), colors.WHITE, 2)

            if object == 'port':
                isShape = find_port(localObj.RATIO, contour, contours, index, img, camera)

            if object == 'ball':
                find_ball(contour, img, localObj.LENGTH)

            # print 'x:%s, y:%s angle:%s ' % ( center_mass_x, center_mass_y, angle )
            distance = get_distance(w, localObj.LENGTH, camera.FOCAL_LENGTH)
            angle = get_angle(camera, center_mass_x, center_mass_y)
            font = cv2.FONT_HERSHEY_DUPLEX
            num_vertices = find_vertices(contour)
            vertices_text = 'vertices:%s' % (num_vertices)
            coordinate_text = 'x:%s y:%s ' % (center_mass_x, center_mass_y)
            area_text = 'area:%s width:%s height:%s' % (area, w, h)
            angle_text = 'angle:%.2f  distance:%s' % (angle, distance)

            cv2.putText(original_img, coordinate_text, (x, y - 35), font, .4, colors.WHITE, 1, cv2.LINE_AA)
            cv2.putText(original_img, area_text, (x, y - 20), font, .4, colors.WHITE, 1, cv2.LINE_AA)
            cv2.putText(original_img, angle_text, (x, y - 5), font, .4, colors.WHITE, 1, cv2.LINE_AA)
            cv2.putText(original_img, vertices_text, (x, y - 50), font, .4, colors.WHITE, 1, cv2.LINE_AA)
            #
            # print 'square: %s,%s' % (w,h)
            # print w/h, h/w
    top_center = (FRAME_WIDTH // 2, FRAME_HEIGHT)
    bottom_center = (FRAME_WIDTH // 2, 0)
    cv2.line(original_img, top_center, bottom_center, colors.WHITE, 4)
    return original_img


def get_angle(camera, x, y):
    a = float(abs(camera.FRAME_WIDTH / 2 - x))
    b = float(camera.FRAME_HEIGHT - y)

    radians = math.atan(a / b)
    angle = radians * 180 / math.pi
    return angle


def get_distance(width_pixel, width_actual, focal_length):
    return focal_length * width_actual / width_pixel


def find_shape(contour, vertices, desired_shape, desired_ratio):
    shape = "unidentified"
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    # print(len(approx))
    # if
    if len(approx) == vertices or len(approx) == vertices - 1 or len(approx) == vertices + 1:
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(approx)
        print(w)
        print(h)
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
            shape = desired_shape
    return shape



def is_not_square(w, h):
    if w > h:
        return float(w) / h > 2
    else:
        return float(h) / w > 2


def find_vertices(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    return len(approx)


def find_bay(size_ratio, contour, contours, index, img, camera):
    x, y, w, h = cv2.boundingRect(contour)
    center_mass_x = x + w / 2
    center_mass_y = y + h / 2
    color = colors.random()
    FRAME_WIDTH = camera.FRAME_WIDTH
    FRAME_HEIGHT = camera.FRAME_HEIGHT
    shape = find_shape(contour, 4, 'bay', size_ratio)
    if shape == 'bay':
        return True
    else:
        return False

def find_port(size_ratio, contour, contours, index, img, camera):
    x, y, w, h = cv2.boundingRect(contour)
    center_mass_x = x + w / 2
    center_mass_y = y + h / 2
    color = colors.random()
    FRAME_WIDTH = camera.FRAME_WIDTH
    FRAME_HEIGHT = camera.FRAME_HEIGHT
    shape = find_shape(contour, 8, 'powerPort', size_ratio)
    if shape == 'powerPort':
        cv2.rectangle(img, (x, y), (x + w, y + h), colors.GREEN, 2)
        cv2.drawContours(img, contours, index, color, 2)
        cv2.circle(img, (int(center_mass_x), int(center_mass_y)), 5, color, -1)
        cv2.line(img, (FRAME_WIDTH // 2, FRAME_HEIGHT), (int(center_mass_x), int(center_mass_y)), color, 2)
    else:
        cv2.rectangle(img, (x, y), (x + w, y + h), colors.WHITE, 2)