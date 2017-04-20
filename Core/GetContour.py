import cv2
import numpy as np
import Utils.CustomOpenCV as ccv
import Setting.DefineManager

def GetContour(Image, drawImage = None):
    contourImage = np.ndarray(Image.shape)
    if drawImage != None:
        contourImage=np.copy(drawImage)
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
def HSVChannelsChange(Image,changeV):
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
    return changeImage

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

    kernel = np.ones((Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 2, Setting.DefineManager.MORPHOLOGY_MASK_SIZE + 2), np.uint8)
    beforeHSVMorph = cv2.morphologyEx(beforeHSVGray, cv2.MORPH_OPEN, kernel)
    afterHSVMorph = cv2.morphologyEx(afterHSVGray, cv2.MORPH_OPEN, kernel)
    # Reduce image noise

    differenceMorph = cv2.absdiff(beforeHSVMorph, afterHSVMorph)
    differenceMorph[differenceMorph > Setting.DefineManager.EACH_IMAGE_DIFFERENCE_THRESHOLD] = Setting.DefineManager.SET_IMAGE_WHITE_COLOR
    differenceMorph[differenceMorph<Setting.DefineManager.SET_IMAGE_WHITE_COLOR] = Setting.DefineManager.SET_IMAGE_BLACK_COLOR
    # Detect each image difference from Morphology Image

    afterDifference = np.copy(differenceMorph)
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

    finalDifference = cv2.absdiff(differenceMorph, afterDifference)

    ccv.ShowImagesWithName([differenceMorph, afterDifference, finalDifference],['Morph','After', 'Difference'])

    return afterDifference