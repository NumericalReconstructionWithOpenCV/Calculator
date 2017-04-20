import cv2

def LoadImageAsGray(pathOfImage):
    tempImage = cv2.imread(pathOfImage)
    tempImage = cv2.cvtColor(tempImage, cv2.COLOR_BGR2GRAY)
    return tempImage

def LoadImage(pathOfImage):
    return cv2.imread(pathOfImage)