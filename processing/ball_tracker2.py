"""
2020 Frc Infinite Recharge
Ball Intake Detection
uses contour lines, rough area calculations
width/height ratios, and radius of contours found
in masked image to find ball
"""

import math
import cv2
from processing import colors
from processing import cvfilters
from processing import shape_util
import time

from profiles import color_profile

import network

MIN_AREA = 1000
BALL_RADIUS = 3.5


debug = False

#
BALL_COLOR_PROFILE = color_profile.ColorProfile()
# 
# BALL_COLOR_PROFILE.hsv_hue.min = 10
# BALL_COLOR_PROFILE.hsv_hue.max = 30
# BALL_COLOR_PROFILE.hsv_sat.min = 124
# BALL_COLOR_PROFILE.hsv_sat.max = 255
# BALL_COLOR_PROFILE.hsv_val.min = 138
# BALL_COLOR_PROFILE.hsv_val.max = 255
#

# yellow_ball.mp4
BALL_COLOR_PROFILE.hsv_hue.min = 19
BALL_COLOR_PROFILE.hsv_hue.max = 134
BALL_COLOR_PROFILE.hsv_sat.min = 115
BALL_COLOR_PROFILE.hsv_sat.max = 255
BALL_COLOR_PROFILE.hsv_val.min = 105
BALL_COLOR_PROFILE.hsv_val.max = 255


def process(img, camera, frame_cnt):
    global rgb_window_active, hsv_window_active

    tracking_data = []
    original_img = img

    img = cv2.GaussianBlur(img, (13, 13), 0)

    img = cvfilters.hsv_threshold(img, BALL_COLOR_PROFILE)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=2)

    if debug:
        cv2.imshow('hsv', img)

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

        #print('%s area:%s' %(index, area) )
        if area > MIN_AREA:
            contour_list.append(contour)
            center_mass_x = x + w / 2
            center_mass_y = y + h / 2
            #
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            (x, y) = (int(x), int(y))
            _, _, w, h = cv2.boundingRect(contour)
            # tests for if its width is around its height which should be true

            # print('x: %s y:%s ratio:%s' % (w, h, w/h))

            if True :
                distance = shape_util.get_distance(w, 2 * radius, camera.FOCAL_LENGTH)
                #convert distance to inches
                distance = 6520 * (w ** -1.02)
                # print(distance * radius ** 2)

                # checks if radius of ball is around actual radius
                if(BALL_RADIUS * 0.9 <= radius <= BALL_RADIUS * 1.10):
                    cv2.circle(original_img, (x, y), int(radius),
                colors.GREEN, 2)
                # print 'x:%s, y:%s angle:%s ' % ( center_mass_x, center_mass_y, angle )
                angle = shape_util.get_angle(camera, center_mass_x, center_mass_y)
                font = cv2.FONT_HERSHEY_DUPLEX

                #labels image
                radius_text = 'radius:%s' % (radius)
                coordinate_text = 'x:%s y:%s ' % (center_mass_x, center_mass_y)
                area_text = 'area:%s width:%s height:%s' % (area, w, h)
                angle_text = 'angle:%.2f  distance:%s' % (angle, distance)

                distance = int(distance)
                angle = int(angle)
                radius = int(radius)

                # set tracking_data
                tracking_data.append(dict(shape='BALL',
                                          radius=radius,
                                          index=index,
                                          dist=int(distance),
                                          angle=angle,
                                          frame=frame_cnt,
                                          xpos=center_mass_x,
                                          ypos=center_mass_y))


                cv2.putText(original_img, coordinate_text, (x, y - 35), font, .4, colors.WHITE, 1, cv2.LINE_AA)
                cv2.putText(original_img, area_text, (x, y - 20), font, .4, colors.WHITE, 1, cv2.LINE_AA)
                cv2.putText(original_img, angle_text, (x, y - 5), font, .4, colors.WHITE, 1, cv2.LINE_AA)
                cv2.putText(original_img, radius_text, (x, y - 50), font, .4, colors.WHITE, 1, cv2.LINE_AA)

                cv2.drawContours(original_img, contours, index, colors.GREEN, 2)
                cv2.circle(original_img, (int(center_mass_x), int(center_mass_y)), 5, colors.GREEN, -1)
                #cv2.line(original_img, (FRAME_WIDTH // 2, FRAME_HEIGHT), (int(center_mass_x), int(center_mass_y)), colors.GREEN, 2)

            #if debug:

                #cv2.drawContours(original_img, contours, index, colors.random(), 2)
                #cv2.rectangle(original_img, (x, y), (x + w, y + h), colors.WHITE, 2)

                # print the rectangle that did not match

            #
            # print 'square: %s,%s' % (w,h)
            # print w/h, h/w
    #top_center = (FRAME_WIDTH // 2, FRAME_HEIGHT)
    #bottom_center = (FRAME_WIDTH // 2, 0)
    #cv2.line(original_img, top_center, bottom_center, colors.WHITE, 4)
    return original_img, tracking_data
