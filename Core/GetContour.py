# -*- coding: utf-8 -*-
import cv2
import numpy as np
import Utils.CustomOpenCV as ccv
import Setting.DefineManager

def FindNavel(contours, drawImage):
    minX = drawImage.shape[1]
    maxX = 0
    maxY = 0
    minY = drawImage.shape[0]
    for contourindex in contours:
        for point in contourindex:
            x, y = point.ravel()
            minX = min(minX,x)
            maxX = max(maxX,x)
            minY = min(minY,y)
            maxY = max(maxY,y)
    x = int((minX + maxX) / 2)
    y = int((minY * Setting.DefineManager.GOLDEN_RATIO + maxY)/(1 + Setting.DefineManager.GOLDEN_RATIO))
    thickness = 0.3
    cv2.circle(drawImage, (x,y), 2, Setting.DefineManager.RGB_COLOR_GREEN, -1)

def AngleAsDealWithPointFromContours(contours, drawImage):
    pointAngle = []
    for contourIndex in contours:
        length = len(contourIndex)
        strideKey = max(length / Setting.DefineManager.RESEARCH_ANGLE_COUNT,Setting.DefineManager.MINIMUM_STRIDE_KEY)
        beforeAngle = 0.0
        for index in range(int(length/strideKey) + 1):
            pointA = contourIndex[((index-1) * strideKey)%length].ravel()
            pointB = contourIndex[((index) * strideKey)%length].ravel()
            pointC = contourIndex[((index+1) * strideKey)%length].ravel()
            x, y = pointB.ravel()
            cv2.circle(drawImage, (x,y), 2, Setting.DefineManager.RGB_COLOR_BLUE, -1)
            nowAngle = AngleBetweenThreePoints(pointA,pointB,pointC)
            absAngle = abs(beforeAngle - nowAngle)
            if absAngle > Setting.DefineManager.ANGLE_AS_DEAL_WITH_POINT :
                pointAngle.append(np.asarray([pointB]))
                angleText = str(int(nowAngle)) + "," + str(int(absAngle))
                thickness = 0.3
                cv2.circle(drawImage, (x,y), 2, Setting.DefineManager.RGB_COLOR_RED, -1)
                cv2.putText(drawImage, angleText,(x,y),0, thickness,Setting.DefineManager.RGB_COLOR_WHITE)
            beforeAngle = nowAngle
    ccv.ShowImagesWithName([drawImage],['PointImage'])
    return pointAngle

#Return angle ABC
def AngleBetweenThreePoints(pointA, pointB, pointC):
    AB = LengthBetweenTwoDots(pointA, pointB)
    BC = LengthBetweenTwoDots(pointB, pointC)
    dot = float(np.sum((pointA - pointB) * (pointC - pointB)))
    cosX = min(max(dot / (AB * BC), -1), 1)
    # For avoid RuntimeWarning: invalid value encountered in arccos
    theta = np.arccos(cosX) * Setting.DefineManager.RADIAN_TO_DEGREE
    #print 'AB : ' + str(AB) + ', BC : ' + str(BC) + ', AB * BC : ' + str(AB*BC) + ', dot : ' + str(dot) + ', cosX : ' + str(cosX),
    #print ', theta : ' + str(theta)
    return theta

def LengthBetweenTwoDots(point1, point2):
    absPoint = (point1 - point2) ** 2
    sumXY = np.sum(absPoint)
    return np.sqrt(sumXY)

# GetMeanRateImage(researchImage)
# 흑백이미지를 입력값으로 받는다
# researchImage를 히스토그램 평활화를 통하여 histImage를 얻는다
# researchImage를 GaussianBlur함수를 통하여 blurImage를 얻는다
# researchImage를 np.uint8형에서 float형으로 변환한 rateImage를 얻는다
# rateImage를 통하여 이미지 화소의 mean(평균값)을 구한다
# rateImage와 mean을 통하여 deviation(편차)를 구한다
# Setting.DefineManager.BASE_DEVIATION과 deviation의비율을 구한다
# 비율을 통하여 새로 구한 rateMean(비율을 통한 평균값)을 구한다
# histImage와 blurImage를 혼합하며 평균차를 더한 rateImage를 구한다.
# cv2.addWeighted(image1, alpha,image2, beta, gamma) = image1 * alpha + image2 * beta + gamma
def GetMeanRateImage(researchImage):
    histImage = cv2.equalizeHist(researchImage)
    blurImage = cv2.GaussianBlur(researchImage,(0,0), Setting.DefineManager.SIGMA)
    rateImage = histImage.astype(float)
    argument = rateImage.shape[0] * rateImage.shape[1]
    mean =  np.sum(rateImage) / argument
    argMean = np.ndarray(rateImage.shape,dtype = float)
    argMean[:] = mean
    calcImage = rateImage - argMean
    deviation = np.sqrt(np.sum(calcImage * calcImage) / argument)
    deviationRate = Setting.DefineManager.BASE_DEVIATION / deviation
    rateMean = mean * deviationRate
    print 'mean : ' + str(mean) + ', deviation : ' + str(deviation)
    rateImage = cv2.addWeighted(histImage, 0.9, blurImage, 0.1, Setting.DefineManager.BASE_MEAN - rateMean)
    return rateImage

# SquareDetectAndReturnRateAsSquare(image)
# 흑백이미지를 입력값으로 받는다
# adaptiveThreshold, Canny, findContours함수 통하여 외곽선을 추출한다
# 찾아진 외곽선 중 사각형으로 추측되는 점들을 rectContour에 담는다
# rectContour를 contourArea(외곽선 영역 넓이)를 통해 오름차순으로 정렬한다
# 순차적으로 영역넓이를 비교해 가며 넓이가 유사한 갯수가 가장 많은 부분을 찾는다
# 높이와 너비가 어느정도 유사한 사각형의 너비를 누적하여 평균값을 낸다
# 위 두 과정은 판넬의 검정색 사각형의 갯수가 유사 갯수의 최대가 된다고 가정
# 평균값을 통하여 resizeRate(이미지를 resize할 비율)을 구한다
def SquareDetectAndReturnRateAsSquare(image):
    binaryImage = cv2.adaptiveThreshold(image, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE * 7, 10)
    edgeImage = cv2.Canny(binaryImage, Setting.DefineManager.CANNY_MINIMUM_THRESHOLD,
                                              Setting.DefineManager.CANNY_MAXIMUM_THRESHOLD, apertureSize=5)

    _, foundContours, h = cv2.findContours(edgeImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    rectContour = []
    for contour in foundContours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4 and cv2.contourArea(contour) > Setting.DefineManager.MINIMUM_RECT_AREA_SIZE :
            rectContour.append(approx)

    # Find Rect Contour
    rectContour = sorted(rectContour, key=cv2.contourArea)
    rectContour.append(rectContour[0])
    maxcount, areaCount, lenghtSum, lenghtMean, beforeAreaSize = [0, 0 ,0, 0, 0];
    for rect in rectContour:
        nowAreaSize = cv2.contourArea(rect)
        rate = float(beforeAreaSize) / float(nowAreaSize)
        if rate < Setting.DefineManager.SIMILAR_RATE or rate > 1.0:
            if areaCount > maxcount:
                maxcount = areaCount
                lenghtMean = lenghtSum / areaCount
            areaCount = 0
            lenghtSum = 0
        areaCount = areaCount + 1
        beforeAreaSize = nowAreaSize
        height = LengthBetweenTwoDots(rect[0][0],rect[1][0])
        width = LengthBetweenTwoDots(rect[1][0],rect[2][0])
        if min(height,width) / max(height,width) > Setting.DefineManager.SIMILAR_RATE:
            lenghtSum = lenghtSum + min(height,width)
    rate = Setting.DefineManager.SQUARE_LENGTH_MEAN / lenghtMean
    print 'rate : ' + str(rate)
    return rate

def GetContour(Image, drawImage = None):
    contourImage = np.ndarray
    if drawImage is not None:
        contourImage=np.copy(drawImage)
    else:
        contourImage = np.ndarray(Image.shape)
    ImageEdgesDetected = cv2.Canny(Image, Setting.DefineManager.CANNY_MINIMUM_THRESHOLD, Setting.DefineManager.CANNY_MAXIMUM_THRESHOLD)
    _, contours, hierarchy = cv2.findContours(ImageEdgesDetected, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(contourImage, contours, -1, 255, 2)
    return contours, contourImage

def GetSharpImage(image):
    Image = np.copy(image)
    if len(Image.shape) <= 2:
        Image = cv2.cvtColor(Image, cv2.COLOR_GRAY2BGR)
    ImageSharp = cv2.GaussianBlur(Image,(0,0), Setting.DefineManager.SIGMA)
    ImageSharp = cv2.addWeighted(Image, Setting.DefineManager.ALPHA,ImageSharp, Setting.DefineManager.BETA, 0)
    ImageSharpGray = cv2.cvtColor(ImageSharp, cv2.COLOR_BGR2GRAY)
    return ImageSharp, ImageSharpGray

#'V'Channel influence 'S'Channel. So, if 'V'Channel is change, 'S'Channel mut be change, too.
# S = C / V , So, if V -> V' S = S * (V / V')
def HSVChannelsChange(Image,changeV,HSV=True):
    if HSV is False:
        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(Image)
    rate = np.ndarray(V.shape, dtype = np.float)
    rate[:] = 1
    rate = rate * V
    V=changeV
    V[V==0] = 1
    rate = rate/V
    rate = rate * S
    S = rate.astype(np.uint8)
    changeImage = cv2.merge([H, S, V])
    if HSV is False:
        image = cv2.cvtColor(Image, cv2.COLOR_HSV2BGR)
        changeImage = cv2.cvtColor(Image, cv2.COLOR_HSV2BGR)
    return changeImage

# NONE
def SimplifyImage(image):
    return image

# FillDifferenceImage(differenceImage)
# 연산을 통하여 얻어낸 차이점 흑백 이미지를 받는다
# =====(반복문)=====
# morpholgyEx의 닫기연산을 통하여 새로운 이미지를 얻는다. 닫기연산 = 팽창연산 후 침식연산
# GaussianBlur를 통하여 차이점 이미지를 다듬는다
# threshold를 통하여 흐려진 이미지를 이진화 하여 뚜렷하게 한다
# 이러한 이미지의 외곽선을 추출하여 외곽선 영역의 갯수를 구한다
# 영역 갯수가 Setting.DefineManager.END_CONTOUR_COUNT보다 작으면 반복문을 종료한다
# =====(반복문)=====
# finalDifference는 처음 받은 differenceImage와 수정한 이미지인 afterDifference의 개선(쇠퇴)부분을 보여준다
def FillDifferenceImage(differenceImage):
    height, width = differenceImage.shape[:]
    afterDifference = np.ndarray((height + Setting.DefineManager.ADD_IMAGE_HEIGHT * 2,width + Setting.DefineManager.ADD_IMAGE_WIDTH * 2),
                                 dtype = differenceImage.dtype)
    afterDifference[:]=Setting.DefineManager.SET_IMAGE_BLACK_COLOR
    afterDifference[Setting.DefineManager.ADD_IMAGE_HEIGHT + height + 15:,
    Setting.DefineManager.ADD_IMAGE_WIDTH:Setting.DefineManager.ADD_IMAGE_WIDTH + width] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    afterDifference[Setting.DefineManager.ADD_IMAGE_HEIGHT:Setting.DefineManager.ADD_IMAGE_HEIGHT + height,
    Setting.DefineManager.ADD_IMAGE_WIDTH:Setting.DefineManager.ADD_IMAGE_WIDTH + width] = differenceImage[:]
    beforeDifference = np.ndarray(afterDifference.shape)
    alpha = 10
    while True:
        kernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE + alpha,Setting.DefineManager.MORPHOLOGY_MASK_SIZE + alpha), np.uint8)
        beforeDifference = np.copy(afterDifference)
        afterDifference = cv2.morphologyEx(afterDifference, cv2.MORPH_CLOSE, kernel)
        afterDifference = cv2.GaussianBlur(afterDifference, (Setting.DefineManager.WIDTH_MASK_SIZE
                                                             , Setting.DefineManager.HEIGHT_MASK_SIZE), 0)
        thresh, afterDifference = cv2.threshold(afterDifference, Setting.DefineManager.THRESHOLD
                                                , Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contourLength = len(GetContour(afterDifference)[0])
        ccv.ShowImagesWithName([beforeDifference,afterDifference],[],700)
        if contourLength < Setting.DefineManager.END_CONTOUR_COUNT:
            break
    afterDifference = afterDifference[Setting.DefineManager.ADD_IMAGE_HEIGHT:Setting.DefineManager.ADD_IMAGE_HEIGHT + height,
    Setting.DefineManager.ADD_IMAGE_WIDTH:Setting.DefineManager.ADD_IMAGE_WIDTH + width]
    finalDifference = cv2.absdiff(differenceImage, afterDifference)

    ccv.ShowImagesWithName([differenceImage, afterDifference, finalDifference],['Before','After', 'Added'])
    return afterDifference

def GetObjectImage(beforeImage, afterImage):
    before = np.copy(beforeImage)
    after = np.copy(afterImage)

    beforeGray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    afterGray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
    #Gray Image

    kernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 2, Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 2), np.uint8)
    beforeMorph = cv2.morphologyEx(beforeGray, cv2.MORPH_OPEN, kernel)
    afterMorph = cv2.morphologyEx(afterGray, cv2.MORPH_OPEN, kernel)
    #Morphology Image

    beforeHSV = cv2.cvtColor(before,cv2.COLOR_BGR2HSV)
    afterHSV = cv2.cvtColor(after,cv2.COLOR_BGR2HSV)
    #HSV Image

    differenceMorph = cv2.absdiff(beforeMorph,afterMorph)
    differenceMorph[differenceMorph>Setting.DefineManager.EACH_IMAGE_DIFFERENCE_THRESHOLD] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    differenceMorph[differenceMorph<Setting.DefineManager.SET_IMAGE_WHITE_COLOR] = Setting.DefineManager.SET_IMAGE_BLACK_COLOR
    absdifferenceMorph = -np.copy(differenceMorph)

    sigmak = 2

    V = cv2.split(beforeHSV)[2]
    V = GetSharpImage(V)[1]
    #V = cv2.GaussianBlur(GetSharpImage(V)[1], (0, 0), sigmak)
    #V[:] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    beforeHSV = HSVChannelsChange(beforeHSV,V)
    beforeHSV = cv2.cvtColor(beforeHSV, cv2.COLOR_HSV2BGR)
    beforeHSVGray = cv2.cvtColor(beforeHSV, cv2.COLOR_BGR2GRAY)

    V = cv2.split(afterHSV)[2]
    V = GetSharpImage(V)[1]
    #V = cv2.GaussianBlur(GetSharpImage(V)[1], (0, 0), sigmak)
    #V[:] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    afterHSV = HSVChannelsChange(afterHSV,V)
    afterHSV = cv2.cvtColor(afterHSV, cv2.COLOR_HSV2BGR)
    afterHSVGray = cv2.cvtColor(afterHSV, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 2, Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 2), np.uint8)
    beforeHSVMorph = cv2.morphologyEx(beforeHSVGray, cv2.MORPH_OPEN, kernel)
    afterHSVMorph = cv2.morphologyEx(afterHSVGray, cv2.MORPH_OPEN, kernel)
    # Reduce image noise

    differenceMorph = cv2.absdiff(beforeHSVMorph, afterHSVMorph)
    differenceMorph[differenceMorph > Setting.DefineManager.EACH_IMAGE_DIFFERENCE_THRESHOLD] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    differenceMorph[differenceMorph<Setting.DefineManager.SET_IMAGE_WHITE_COLOR] = Setting.DefineManager.SET_IMAGE_BLACK_COLOR
    # Detect each image difference from Morphology Image

    objectImage = FillDifferenceImage(differenceMorph)

    return objectImage