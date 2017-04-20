# -*- coding: utf-8 -*-
import cv2
import numpy as np

import ColorDetect
import ImageMatrixMove
import Setting.DefineManager
import ShapeDetectAndFindCorner
from Utils import LogManager, CustomOpenCV
from Setting import DefineManager

import GetContour

def DetectBlackBoardContourFromOriginImage(targetImage):

    targetGrayImage = cv2.cvtColor(targetImage, cv2.COLOR_BGR2GRAY)
    # Change color to gray

    morpholgyKernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE, Setting.DefineManager.MORPHOLOGY_MASK_SIZE), np.uint8)
    targetMorphologyGrayImage = cv2.morphologyEx(targetGrayImage, cv2.MORPH_OPEN, morpholgyKernel)
    # Reduce image noise

    targetMorphologyGrayImage = cv2.adaptiveThreshold(targetMorphologyGrayImage, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE, 10)
    # Get small size of block's threshold value

    targetEdgeMorphologyGrayImage = cv2.Canny(targetMorphologyGrayImage, Setting.DefineManager.CANNY_MINIMUM_THRESHOLD, Setting.DefineManager.CANNY_MAXIMUM_THRESHOLD, apertureSize = 5)

    # Edge detect from bulr processed image
    (_, beforeEdgeGrayImageContour, h) = cv2.findContours(targetEdgeMorphologyGrayImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Get image contour

    foundedMaxAreaSizeContours = sorted(beforeEdgeGrayImageContour, key=cv2.contourArea, reverse=True)[:Setting.DefineManager.GET_MAXIMUM_AREA_SIZE]

    return FindSquareObjectFromContourData(foundedMaxAreaSizeContours)

def FindSquareObjectFromContourData(contourDatas):
    for indexOfContour in contourDatas:
        peri = cv2.arcLength(indexOfContour, True)
        approx = cv2.approxPolyDP(indexOfContour, 0.02 * peri, True)

        if len(approx) == Setting.DefineManager.SQUARE_CORNER_NUM:
            squareContourData = approx
            LogManager.PrintLog("ObjectDetect", "FindSquareObjectFromContourData", "Square Contour Data Founded", DefineManager.LOG_LEVEL_INFO)
            return squareContourData
    LogManager.PrintLog("ObjectDetect", "FindSquareObjectFromContourData", "Square Contour Data Not Founded", DefineManager.LOG_LEVEL_WARN)
    return None


def DetectObjectFromImage(beforeImage, afterImage):

    squareContourData = DetectBlackBoardContourFromOriginImage(beforeImage)

    # 굴곡진 큰 사각형 정사각형으로 보정
    perspectiveUpdatedBeforeImage = ImageMatrixMove.ImageMatrixMove(beforeImage, squareContourData)
    perspectiveUpdatedAfterImage = ImageMatrixMove.ImageMatrixMove(afterImage, squareContourData)

    CustomOpenCV.ShowImagesWithName([perspectiveUpdatedBeforeImage, perspectiveUpdatedAfterImage],
                                    ["perspectiveUpdatedBeforeImage", "perspectiveUpdatedAfterImage"])


    # 작은 사각형과 그 모서리 찾기
    croppedBeforeCorner = ShapeDetectAndFindCorner.ShapeDetectAndFindCorner(perspectiveUpdatedBeforeImage)

    height, width = perspectiveUpdatedBeforeImage.shape[:2]
    rate = Setting.DefineManager.IMAGE_WIDTH / width
    resizeBefore = cv2.resize(perspectiveUpdatedBeforeImage, (int(Setting.DefineManager.IMAGE_WIDTH),int(rate * height)))
    height, width = perspectiveUpdatedAfterImage.shape[:2]
    rate = Setting.DefineManager.IMAGE_WIDTH / width
    resizeAfter = cv2.resize(perspectiveUpdatedAfterImage, (int(Setting.DefineManager.IMAGE_WIDTH),int(rate * height)))
    # Resize Image

    beforeGray = cv2.cvtColor(resizeBefore, cv2.COLOR_BGR2GRAY)
    afterGray = cv2.cvtColor(resizeAfter, cv2.COLOR_BGR2GRAY)
    # Change color to gray

    kernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 1, Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 1), np.uint8)
    beforeMorph = cv2.morphologyEx(beforeGray, cv2.MORPH_OPEN, kernel)
    afterMorph = cv2.morphologyEx(afterGray, cv2.MORPH_OPEN, kernel)
    # Reduce image noise

    differenceMorph = cv2.absdiff(beforeMorph, afterMorph)
    differenceMorph[differenceMorph > Setting.DefineManager.EACH_IMAGE_DIFFERENCE_THRESHOLD] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    # Detect each image difference from Morphology Image

    beforeThresh = cv2.adaptiveThreshold(beforeMorph, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE, 10)
    afterThresh = cv2.adaptiveThreshold(afterMorph, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE, 10)
    # Adaptive Threshold Image

    differenceThresh = cv2.absdiff(beforeThresh, afterThresh)
    differenceThresh[differenceThresh > Setting.DefineManager.EACH_IMAGE_DIFFERENCE_THRESHOLD] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    # Detect each image difference from Threshold Image

    CustomOpenCV.ShowImagesWithName([beforeThresh,afterThresh],['before','after'])
    CustomOpenCV.ShowImagesWithName([differenceMorph, differenceThresh], ['Morph','Thresh'])

    # for count in contours:
    #     approx = cv2.approxPolyDP(count, 0.1 * cv2.arcLength(count, True), True)
    #     if len(approx) == 5 :
    #         find pentagon
            # cv2.drawContours(lineImage, [count], 0, (255, 0, 0), -1)
        # elif len(approx) == 3 :
        #     find triangle
            # cv2.drawContours(lineImage, [count], 0, (0, 255, 0), -1)
        # elif len(approx) == 4 :
        #     find square
            # cv2.drawContours(lineImage, [count], 0, (0, 0, 255), -1)  # square
            # for i in approx:
            #     x, y = i.ravel()
            #     cv2.circle(lineImage, (x, y), 1, (0, 255, 0), -1)

    # contour, contourImage = GetContour.GetContour(differenceMorph)
    #Utils.CustomOpenCV.ShowImagesWithName([differenceMorph,contourImage])

    return  resizeBefore, resizeAfter, differenceMorph, differenceThresh


    # mask = ColorDetect.ColorDetectFromImage(testcase + "before.jpg")

    # plt.imshow(afterGrayImage)

    # differenceBetweenLoadedImages = cv2.absdiff(beforeImage, afterImage)
    #
    # diff = afterImage - beforeImage
    #
    # differenceBetweenLoadedImages[differenceBetweenLoadedImages > 40] = 255
    #
    # differenceBetweenLoadedImages = cv2.cvtColor(differenceBetweenLoadedImages, cv2.COLOR_BGR2GRAY)
    #
    # last_result = differenceBetweenLoadedImages - mask
    #
    # cv2.imwrite((testcase + "result_absdiff.jpg"), differenceBetweenLoadedImages)
    #
    # cv2.imwrite((testcase + "result_mask.jpg"), mask)
    #
    # cv2.imwrite((testcase + "result_diff2.jpg"), last_result)
    #
    # blurKernel = cv2.GaussianBlur(differenceBetweenLoadedImages, (3, 3), 0)
    #
    # differenceBetweenLoadedImages = cv2.adaptiveThreshold(differenceBetweenLoadedImages, 255,
    #                                                       cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 10)
    #
    # imageEdgesDetected = cv2.Canny(differenceBetweenLoadedImages, 0, 255)
    #
    # _, contours, hierarchy = cv2.findContours(imageEdgesDetected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #
    # maxContoursArea = 0
    # calculatedContourArea = 0
    # maxContoursIndex = []
    # for contoursIndex in contours:
    #     calculatedContourArea = cv2.contourArea(contoursIndex)
    #     if maxContoursArea < calculatedContourArea:
    #         maxContoursArea = calculatedContourArea
    #         maxContoursIndex = contoursIndex
    #
    # cv2.drawContours(beforeImage, contours, 0, 255, 3)
    #
    # (positionX, positionY, width, height) = cv2.boundingRect(maxContoursIndex)
    #
    # cv2.rectangle(beforeImage, (positionX, positionY), (positionX + width, positionY + height), 255, 2)
    #
    # cv2.imwrite("Resources/testcase2/result.jpg", beforeGrayImage)