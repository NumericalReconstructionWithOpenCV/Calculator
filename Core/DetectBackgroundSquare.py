# -*- coding: utf-8 -*-
# 색상 검출하는 프로그램
import cv2
import numpy as np
import imutils
import ColorDetect

def DetectBackgroundSquareFromImage(image):
    imageFromDetectedColor = ColorDetect.ColorDetectFromImage(image, [40, 100, 100], [60, 255, 255])

    gray = cv2.cvtColor(imageFromDetectedColor, cv2.COLOR_BGR2GRAY)

    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]

    _, contours, h = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centerPoint = []
    for count in contours:
        M = cv2.moments(count)
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        centerPoint.append([cX, cY])

        cv2.drawContours(imageFromDetectedColor, [count], -1, (255, 0, 0), 2)
        cv2.circle(imageFromDetectedColor, (cX, cY), 7, (0, 255, 0), -1)
        cv2.putText(imageFromDetectedColor, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    ctrNp = np.array(centerPoint).reshape((-1,1,2)).astype(np.int32)
    #cv2.imwrite("../Tests/practice/out1.jpg", imageFromDetectedColor)
    cv2.imshow("abcdef", imageFromDetectedColor)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    return ctrNp
