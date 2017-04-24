import cv2
import numpy as np

#Show Images. If there is no title, Window name is 'image+alpha'
def ShowImagesWithName(image, title = [], key=0):
    cv2.destroyAllWindows()
    cnt = len(image)
    for k in range(cnt):
        string = ''
        if len(title) < k + 1:
            string = 'image' + str(k)
        else:
            string = title[k]
        cv2.imshow(string, image[k])
    cv2.waitKey(key)

# Resize Image as rate
def ResizeImageAsRate(image, resizeRate):
    resizeImage = np.copy(image)
    height, width = image.shape[:2]
    resizeImage = cv2.resize(resizeImage, (int(resizeRate * width),int(resizeRate * height)))
    return resizeImage

# Resize Image as width
def ResizeImageAsWidth(image, resizeWidth):
    resizeImage = np.copy(image)
    height, width = image.shape[:2]
    rate = resizeWidth / width
    resizeImage = cv2.resize(resizeImage, (int(resizeWidth),int(rate * height)))
    return resizeImage