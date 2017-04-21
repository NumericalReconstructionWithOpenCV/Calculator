# -*- coding: utf-8 -*-
# 색상 검출하는 프로그램
import cv2
import numpy as np

def ColorDetectFromImage(image, lower_hsv, upper_hsv):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array(lower_hsv, dtype=np.uint8)
    upper = np.array(upper_hsv, dtype=np.uint8)

    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask=mask)

    #cv2.imwrite(arg2,  mask)

    return res