# -*- coding: utf-8 -*-
# 색상 검출하는 프로그램
import cv2
import numpy as np

def ColorDetectFromImage(arg1):
    origin_image = cv2.imread(arg1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(origin_image, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([  0,  0,100], dtype=np.uint8)
    upper_blue = np.array([255,255,255], dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(origin_image, origin_image, mask=mask)

    #cv2.imwrite(arg2,  mask)

    return mask