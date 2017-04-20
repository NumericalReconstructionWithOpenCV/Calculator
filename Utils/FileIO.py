import cv2

def LoadImageAsGray(pathOfImage):
    return cv2.imread(pathOfImage, cv2.COLOR_BGR2GRAY)

def LoadImage(pathOfImage):
    return cv2.imread(pathOfImage)