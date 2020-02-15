"""
2020 Frc Infinite Recharge
Port Intake Detection
uses contour lines and 
rough width/length ratios, area, 
and vertices to check a masked image
for the port

same as bay tracker but with diff.
object dimensions
"""

import math
import cv2
from processing import colors
from processing import cvfilters
from processing import shape_util
import time

from profiles import color_profiles

MIN_AREA = 10
PORT_LENGTH = 39.25

# 
WIDTH_TO_HEIGHT_RATIO = 39.25 / 17

debug = False

def process(img, camera, frame_cnt, color_profile):
    global rgb_window_active, hsv_window_active

    FRAME_WIDTH = camera.FRAME_WIDTH
    FRAME_HEIGHT = camera.FRAME_HEIGHT
    
    tracking_data = []
    original_img = img

    img = cv2.GaussianBlur(img, (13, 13), 0)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_mask = cvfilters.hsv_threshold(img, color_profile)
    img = cv2.bitwise_and(img, img, hsv_mask)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # if debug:
    #     cv2.imshow('hsv', img)


    _, contours, hierarchy = cv2.findContours(img,
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
            if shape_util.dimensions_match(contour, 6,2, WIDTH_TO_HEIGHT_RATIO):
                # print 'x:%s, y:%s angle:%s ' % ( center_mass_x, center_mass_y, angle )
                distance = shape_util.distance_in_inches_long(w)
                angle = shape_util.get_angle(camera, center_mass_x, center_mass_y)
                font = cv2.FONT_HERSHEY_DUPLEX

                # set tracking_data
                data = dict(shape='BAY',
                        width=w,
                        height=h,
                        dist=distance,
                        angle=angle,
                        xpos=center_mass_x,
                        ypos=center_mass_y)

                tracking_data.append(data)
                
                num_vertices = shape_util.find_vertices(contour)
                vertices_text = 'vertices:%s' % (num_vertices)
                coordinate_text = 'x:%s y:%s ' % (center_mass_x, center_mass_y)
                area_text = 'area:%s width:%s height:%s' % (area, w, h)
                angle_text = 'angle:%.2f  distance:%.2f' % (angle, distance)

                cv2.putText(original_img, coordinate_text, (x, y - 35), font, .4, colors.WHITE, 1, cv2.LINE_AA)
                cv2.putText(original_img, area_text, (x, y - 20), font, .4, colors.WHITE, 1, cv2.LINE_AA)
                cv2.putText(original_img, angle_text, (x, y - 5), font, .4, colors.WHITE, 1, cv2.LINE_AA)

                cv2.rectangle(original_img, (x, y), (x + w, y + h), colors.GREEN, 2)
                cv2.drawContours(original_img, contours, index, colors.random(), 2)
                cv2.circle(original_img, (int(center_mass_x), int(center_mass_y)), 5, colors.GREEN, -1)
                cv2.line(original_img, (FRAME_WIDTH // 2, FRAME_HEIGHT), (int(center_mass_x), int(center_mass_y)), colors.GREEN, 2)

            elif debug:
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.drawContours(original_img, contours, index, colors.random(), 2)
                num_vertices = shape_util.find_vertices(contour)
                vertices_text = 'vertices:%s' % (num_vertices)
                cv2.putText(original_img, vertices_text, (x, y - 50), font, .4, colors.WHITE, 1, cv2.LINE_AA)
                #cv2.rectangle(original_img, (x, y), (x + w, y + h), colors.WHITE, 2)

                # print the rectangle that did not match

            #
            # print 'square: %s,%s' % (w,h)
            # print w/h, h/w
    top_center = (FRAME_WIDTH // 2, FRAME_HEIGHT)
    bottom_center = (FRAME_WIDTH // 2, 0)
    cv2.line(original_img, top_center, bottom_center, colors.WHITE, 4)
    return original_img, tracking_data


