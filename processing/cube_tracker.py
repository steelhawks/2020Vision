"""

Object Tracker based on a color profile

uses contour lines and rough area calculations

"""

import cv2
import math
from processing import colors
from processing import filters
from profiles import yellow_profile

MIN_SQUARE_AREA = 400

CUBE_LENGTH = 13

def process(img,
            camera,
            profile=yellow_profile):

    FRAME_WIDTH = camera.FRAME_WIDTH
    FRAME_HEIGHT = camera.FRAME_HEIGHT

    img = filters.resize(img, camera.FRAME_WIDTH, camera.FRAME_HEIGHT )

    original_img = img

    rgb_mask = filters.rgb_threshold(img, profile)

    img = filters.apply_mask(img, rgb_mask)

    img = filters.hsv_threshold(img, profile)

    img = filters.median_filter(img)

    _, contours, hierarchy = cv2.findContours(img,
                                              cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)

    contour_list = []
    for (index,contour) in enumerate(contours):

        area = cv2.contourArea(contour)
        # peri = cv2.arcLength(contour, True)
        # approx = cv2.approxPolyDP(contour, 0.04 * peri, True)

        #
        # limit the number of contours to process
        #
        if area > MIN_SQUARE_AREA:
            contour_list.append(contour)

            color = colors.random()

            x,y,w,h = cv2.boundingRect(contour)

            #
            # if it is a cube, then outbound rectangle should be close to a square
            #
            if is_not_square(w,h):
                cv2.rectangle(original_img, (x, y), (x + w, y + h), colors.WHITE, 2)
                continue

            cv2.rectangle(original_img,(x,y),(x+w,y+h),colors.GREEN ,2)
            #
            # print 'square: %s,%s' % (w,h)
            # print w/h, h/w

            center_mass_x = x+w/2
            center_mass_y = y+h/2

            angle = get_angle( camera, center_mass_x, center_mass_y )
            distance = get_distance(w, CUBE_LENGTH, camera.FOCAL_LENGTH)

            # print 'x:%s, y:%s angle:%s ' % ( center_mass_x, center_mass_y, angle )

            cv2.drawContours(original_img, contours,  index, color, 2)
            cv2.circle(original_img, (center_mass_x, center_mass_y),5,color, -1);
            cv2.line(original_img,(FRAME_WIDTH/2,FRAME_HEIGHT),(center_mass_x,center_mass_y),color,2)

            font = cv2.FONT_HERSHEY_DUPLEX

            coordinate_text = 'x:%s y:%s ' % ( center_mass_x, center_mass_y)
            area_text = 'area:%s width:%s' % (area,w)
            angle_text = 'angle:%.2f  distance:%s' % (angle, distance)

            cv2.putText(original_img, coordinate_text, (x,y-35), font, .4, colors.WHITE , 1, cv2.LINE_AA)
            cv2.putText(original_img, area_text, (x, y-20), font, .4, colors.WHITE, 1, cv2.LINE_AA)
            cv2.putText(original_img, angle_text, (x, y - 5), font, .4, colors.WHITE, 1, cv2.LINE_AA)

    # create a line for the center of frame
    cv2.line(original_img, (FRAME_WIDTH / 2, FRAME_HEIGHT), (FRAME_WIDTH/2, 0), colors.WHITE, 4)

    return original_img


def get_angle( camera, x, y ):

    a = float(abs(camera.FRAME_WIDTH/2 - x ))
    b = float(camera.FRAME_HEIGHT - y)

    radians = math.atan(a/b)
    angle = radians * 180 / math.pi
    return angle


def get_distance( width_pixel, width_actual, focal_length ):

    return focal_length * width_actual / width_pixel


def is_not_square(w,h):
    if w > h:
       return float(w)/h > 2
    else:
        return float(h)/w > 2