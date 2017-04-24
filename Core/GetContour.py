import cv2
import numpy as np
import Utils.CustomOpenCV as ccv
import Setting.DefineManager

#Return angle ABC
def AngleBetweenThreePoints(pointA, pointB, pointC):
    AB = LengthBetweenTwoDots(pointA, pointB)
    BC = LengthBetweenTwoDots(pointB, pointC)
    dot = float(np.sum((pointA - pointB) * (pointC - pointB)))
    theta = np.arccos(dot/(AB*BC))
    return theta * Setting.DefineManager.RADIAN_TO_DEGREE

def LengthBetweenTwoDots(point1, point2):
    absPoint = (point1 - point2) ** 2
    sumXY = np.sum(absPoint)
    return np.sqrt(sumXY)

def GetMeanRateImage(researchImage):
    histImage = cv2.equalizeHist(researchImage)
    rateImage = histImage.astype(float)
    argument = rateImage.shape[0] * rateImage.shape[1]
    mean =  np.sum(rateImage) / argument
    argMean = np.ndarray(rateImage.shape,dtype = float)
    argMean[:] = mean
    calcImage = rateImage - argMean
    dispersion = np.sqrt(np.sum(calcImage * calcImage) / argument)
    dispersionRate = Setting.DefineManager.BASE_DISPERSION / dispersion
    rateMean = mean * dispersionRate
    print 'mean : ' + str(mean) + ', dispersion : ' + str(dispersion)
    blurImage = cv2.GaussianBlur(researchImage,(0,0), Setting.DefineManager.SIGMA)
    rateImage = cv2.addWeighted(histImage, 0.9, blurImage, 0.1, Setting.DefineManager.BASE_MEAN - rateMean)
    return rateImage

def SquareDetectAndReturnRateAsSquare(image):
    binaryImage = cv2.adaptiveThreshold(image, Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, Setting.DefineManager.NEIGHBORHOOD_MASK_SIZE * 7, 10)
    edgeImage = cv2.Canny(binaryImage, Setting.DefineManager.CANNY_MINIMUM_THRESHOLD,
                                              Setting.DefineManager.CANNY_MAXIMUM_THRESHOLD, apertureSize=5)
    ccv.ShowImagesWithName([edgeImage])
    _, foundContours, h = cv2.findContours(edgeImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    rectContour = []
    for contour in foundContours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4 and cv2.contourArea(contour) > Setting.DefineManager.MINIMUM_RECT_AREA_SIZE :
            rectContour.insert(len(rectContour) - 1, approx)
    ccv.ShowImagesWithName([image])
    # Find Rect Contour
    rectContour = sorted(rectContour, key=cv2.contourArea)
    rectContour.insert(len(rectContour),rectContour[0])
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

    '''
    maxContoursArea = 0
    calculatedContourArea = 0
    maxContoursIndex = []
    for contoursIndex in contours:
        calculatedContourArea = cv2.contourArea(contoursIndex)
        if maxContoursArea < calculatedContourArea:
            maxContoursArea = calculatedContourArea
            maxContoursIndex = contoursIndex
    '''

    cv2.drawContours(contourImage, contours, -1, 255, 2)
    return contours, contourImage

def GetSharpImage(image):
    Image = np.copy(image)
    if len(Image.shape) <= 2:
        Image = cv2.cvtColor(Image, cv2.COLOR_GRAY2BGR)
    ImageSharp = cv2.GaussianBlur(Image,(0,0), Setting.DefineManager.SIGMA)
    ImageSharp = cv2.addWeighted(Image, Setting.DefineManager.ALPHA,ImageSharp, Setting.DefineManager.BETA,0)
    ImageSharpGray = cv2.cvtColor(ImageSharp, cv2.COLOR_BGR2GRAY)
    #Show([ImageSharp, ImageSharpGray],['Sharp','SharpGray'])
    return ImageSharp, ImageSharpGray

#'V'Channel influence 'S'Channel. So, if 'V'Channel is change, 'S'Channel mut be change, too.
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

def SimplifyImage(image):
    return image

def FillDifferenceImage(differenceImage):
    afterDifference = np.copy(differenceImage)
    beforeDifference = np.ndarray(afterDifference.shape)
    count = 10
    sameCount = 0
    beforeCount = 0
    while True:
        kernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE + count,Setting.DefineManager.MORPHOLOGY_MASK_SIZE + count), np.uint8)
        beforeDifference = np.copy(afterDifference)
        afterDifference = cv2.morphologyEx(afterDifference, cv2.MORPH_CLOSE, kernel)
        afterDifference = cv2.GaussianBlur(afterDifference, (Setting.DefineManager.BLUR_MASK_SIZE * Setting.DefineManager.WIDTH_MULTIPLE
                                                             ,Setting.DefineManager.BLUR_MASK_SIZE  * Setting.DefineManager.HEIGHT_MULTIPLE), 0)
        thresh, afterDifference = cv2.threshold(afterDifference, Setting.DefineManager.THRESHOLD
                                                , Setting.DefineManager.SET_IMAGE_WHITE_COLOR, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        diff = -cv2.absdiff(beforeDifference, afterDifference).astype(np.bool)
        nowCount = len(GetContour(afterDifference)[0])
        if diff.all() or sameCount >= 5:
            count = count + 2
            sameCount = 0
        if beforeCount == nowCount:
            sameCount = sameCount + 1
        else:
            sameCount = 0
        print nowCount
        if nowCount < Setting.DefineManager.END_CONTOUR_COUNT:
            break
        beforeCount = nowCount

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

    V = cv2.split(beforeHSV)[2]
    V = GetSharpImage(V)[1]
    beforeHSV = HSVChannelsChange(beforeHSV,V)
    beforeHSV = cv2.cvtColor(beforeHSV, cv2.COLOR_HSV2BGR)
    beforeHSVGray = cv2.cvtColor(beforeHSV, cv2.COLOR_BGR2GRAY)

    V = cv2.split(afterHSV)[2]
    V = GetSharpImage(V)[1]
    afterHSV = HSVChannelsChange(afterHSV,V)
    afterHSV = cv2.cvtColor(afterHSV, cv2.COLOR_HSV2BGR)
    afterHSVGray = cv2.cvtColor(afterHSV, cv2.COLOR_BGR2GRAY)

    ccv.ShowImagesWithName([after,afterHSV])

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