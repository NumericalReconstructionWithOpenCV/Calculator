import cv2
import numpy as np

def FindCornerFromImage(testcase):
    img = cv2.imread(testcase + "result_mask.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners = cv2.goodFeaturesToTrack(gray, 5000, 0.3, 3)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)

    cv2.imwrite(testcase + "result_corner.jpg", img)