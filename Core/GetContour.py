import cv2
import numpy as np
import Utils.CustomOpenCV as ccv
import Setting.DefineManager

def GetContour(Image):
    contourImage = np.ndarray(Image.shape)
    ImageEdgesDetected = cv2.Canny(Image, Setting.DefineManager.CANNY_MINIMUM_THRESHOLD, Setting.DefineManager.CANNY_MAXIMUM_THRESHOLD)
    _, contours, hierarchy = cv2.findContours(ImageEdgesDetected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #ccv.ShowImagesWithName([ImageEdgesDetected])
    maxContoursArea = 0
    calculatedContourArea = 0
    maxContoursIndex = []
    for contoursIndex in contours:
        calculatedContourArea = cv2.contourArea(contoursIndex)
        if maxContoursArea < calculatedContourArea:
            maxContoursArea = calculatedContourArea
            maxContoursIndex = contoursIndex

    cv2.drawContours(contourImage, contours, -1, 255, 3)
    return contours, contourImage