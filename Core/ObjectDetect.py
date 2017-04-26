# -*- coding: utf-8 -*-
import cv2
import numpy as np

import ImageMatrixMove
import Setting.DefineManager
import ShapeDetectAndFindCorner
import DetectBackgroundSquare
from Utils import LogManager, CustomOpenCV
from Setting import DefineManager

import GetContour

def DetectBlackBoardContourFromOriginImage(targetGrayImage):

    targetEqualizeGrayImage = GetContour.GetMeanRateImage(targetGrayImage)

    morpholgyKernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE, Setting.DefineManager.MORPHOLOGY_MASK_SIZE), np.uint8)
    targetMorphologyGrayImage = cv2.morphologyEx(targetEqualizeGrayImage, cv2.MORPH_OPEN, morpholgyKernel)
    # Reduce image noise

    targetMorphologyGrayImage = cv2.adaptiveThreshold(targetMorphologyGrayImage, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE, 10)
    # Get small size of block's threshold value

    targetEdgeMorphologyGrayImage = cv2.Canny(targetMorphologyGrayImage, Setting.DefineManager.CANNY_MINIMUM_THRESHOLD, Setting.DefineManager.CANNY_MAXIMUM_THRESHOLD, apertureSize = 5)

    #CustomOpenCV.ShowImagesWithName([CustomOpenCV.ResizeImageAsRate(targetEdgeMorphologyGrayImage,0.7)], ["targetEdgeMorphologyGrayImage"])

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


def DetectObjectFromImage(beforeImage, afterImage, beforeGrayImage, afterGrayImage):

    resizeRate = GetContour.SquareDetectAndReturnRateAsSquare(beforeGrayImage)
    beforeImage = CustomOpenCV.ResizeImageAsRate(beforeImage,resizeRate)
    beforeGrayImage = CustomOpenCV.ResizeImageAsRate(beforeGrayImage,resizeRate)
    afterImage = CustomOpenCV.ResizeImageAsRate(afterImage,resizeRate)
    afterGrayImage = CustomOpenCV.ResizeImageAsRate(afterGrayImage,resizeRate)

    #squareContourData = DetectBackgroundSquare.DetectBackgroundSquareFromImage(beforeImage) 형광색 인식으로 점 4개 찾는 함수
    squareContourData = DetectBlackBoardContourFromOriginImage(beforeGrayImage)

    # 굴곡진 큰 사각형 정사각형으로 보정
    perspectiveUpdatedBeforeImage = ImageMatrixMove.ImageMatrixMove(beforeImage, squareContourData)
    perspectiveUpdatedAfterImage = ImageMatrixMove.ImageMatrixMove(afterImage, squareContourData)

    perspectiveUpdatedBeforeImage = CustomOpenCV.ResizeImageAsWidth(perspectiveUpdatedBeforeImage, DefineManager.IMAGE_WIDTH)
    perspectiveUpdatedAfterImage = CustomOpenCV.ResizeImageAsWidth(perspectiveUpdatedAfterImage, DefineManager.IMAGE_WIDTH)
    # Resize image as shape [ rateHeight, DefineManager.IMAGE_WIDTH ]

    #CustomOpenCV.ShowImagesWithName([perspectiveUpdatedBeforeImage, perspectiveUpdatedAfterImage],
    #                                ["perspectiveUpdatedBeforeImage", "perspectiveUpdatedAfterImage"])

    perspectiveUpdatedBeforeGrayImage = cv2.cvtColor(perspectiveUpdatedBeforeImage, cv2.COLOR_BGR2GRAY)
    perspectiveUpdatedAfterGrayImage = cv2.cvtColor(perspectiveUpdatedAfterImage, cv2.COLOR_BGR2GRAY)

    morphologyKernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 1, Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 1), np.uint8)
    perspectiveUpdatedBeforeMorphologyGrayImage = cv2.morphologyEx(perspectiveUpdatedBeforeGrayImage, cv2.MORPH_OPEN, morphologyKernel)
    perspectiveUpdatedAfterMorphologyGrayImage = cv2.morphologyEx(perspectiveUpdatedAfterGrayImage, cv2.MORPH_OPEN, morphologyKernel)
    # Reduce image noise

    beforeThresholdedBlackBoardImage = cv2.adaptiveThreshold(perspectiveUpdatedBeforeMorphologyGrayImage, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE, 10)
    afterThresholdedBlackBoardImage = cv2.adaptiveThreshold(perspectiveUpdatedAfterMorphologyGrayImage, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE, 10)
    # Adaptive Threshold Image
    #CustomOpenCV.ShowImagesWithName([beforeThresholdedBlackBoardImage, afterThresholdedBlackBoardImage], ['beforeThresholdedBlackBoardImage', 'afterThresholdedBlackBoardImage'])

    differenceBasedOnThreshImage = cv2.absdiff(beforeThresholdedBlackBoardImage, afterThresholdedBlackBoardImage)
    differenceBasedOnThreshImage[differenceBasedOnThreshImage > Setting.DefineManager.EACH_IMAGE_DIFFERENCE_THRESHOLD] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    # Detect each image difference from Threshold Image


    #CustomOpenCV.ShowImagesWithName([differenceBasedOnThreshImage], ["differenceBasedOnThreshImage"])
    objectFoundedImage = GetContour.GetObjectImage(perspectiveUpdatedBeforeImage, perspectiveUpdatedAfterImage)

    humanDetectedContour, contourLineDrawImage = GetContour.GetContour(objectFoundedImage, perspectiveUpdatedAfterImage)
    GetContour.FindNavel(humanDetectedContour,contourLineDrawImage)
    importantPoint = GetContour.AngleAsDealWithPointFromContours(humanDetectedContour,contourLineDrawImage)

    return [beforeThresholdedBlackBoardImage, afterThresholdedBlackBoardImage, differenceBasedOnThreshImage, humanDetectedContour]

def FindSmallBoxesFromBlackBoardImage(perspectiveUpdatedBeforeImage):
    # 작은 사각형과 그 모서리 찾기
    smallRectangleFoundedImage = ShapeDetectAndFindCorner.ShapeDetectAndFindCorner(perspectiveUpdatedBeforeImage)
    return smallRectangleFoundedImage

    # CustomOpenCV.ShowImagesWithName([differenceBetweenEachImages, differenceThresh], ['Morph','Thresh'])

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

    # return  resizeBefore, resizeAfter, differenceMorph, differenceThresh


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