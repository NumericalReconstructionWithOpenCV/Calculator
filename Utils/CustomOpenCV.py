import cv2

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