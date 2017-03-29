import cv2
import unittest2 as unittest
from matplotlib import pyplot as plt

def DetectObjectFromImage(beforeImage, afterImage):
    return []

def Detecting():
    beforeGrayImage = cv2.imread('Resources/beforeImage.png',0)

    #beforeGrayImage = cv2.cvtColor(beforeImage, cv2.COLOR_BGR2GRAY)

    afterGrayImage = cv2.imread('Resources/afterImage.png',0)

    #cv2.imwrite('Testing.jpg',afterGrayImage)

    #afterGrayImage = cv2.cvtColor(afterImage, cv2.COLOR_BGR2GRAY)

    #plt.imshow(afterGrayImage, cmap="gray")

    differenceBetweenLoadedImages = cv2.absdiff(beforeGrayImage, afterGrayImage)

    differenceBetweenLoadedImages[differenceBetweenLoadedImages > 0] = 255

    blurKernel = cv2.GaussianBlur(differenceBetweenLoadedImages, (3, 3), 0)

    differenceBetweenLoadedImages = cv2.adaptiveThreshold(differenceBetweenLoadedImages, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 10)

    plt.imshow(differenceBetweenLoadedImages, cmap="gray")

    imageEdgesDetected = cv2.Canny(differenceBetweenLoadedImages, 0, 255)

    _, contours, hierarchy = cv2.findContours(imageEdgesDetected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    maxContoursArea = 0
    calculatedContourArea = 0
    maxContoursIndex = []
    for contoursIndex in contours:
        calculatedContourArea = cv2.contourArea(contoursIndex)
        if maxContoursArea < calculatedContourArea:
            maxContoursArea = calculatedContourArea
            maxContoursIndex = contoursIndex
    print maxContoursIndex, maxContoursArea

    cv2.drawContours(beforeGrayImage, [maxContoursIndex], 0, 255, 3)

    plt.imshow(beforeGrayImage, cmap="gray")

    (positionX, positionY, width, height) = cv2.boundingRect(maxContoursIndex)
    print positionX, positionY, width, height

    cv2.rectangle(beforeGrayImage, (positionX, positionY), (positionX + width, positionY + height), 255, 2)

    cv2.imwrite('Resources/End',beforeGrayImage, cmap="gray")