import cv2

def ShapeDetectAndFindCorner(arg_image):
    gray = cv2.cvtColor(arg_image, cv2.COLOR_BGR2GRAY)
    gray = 255 - gray

    ret, thresh = cv2.threshold(gray, 127, 255, 1)

    _, contours, h = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for count in contours:
        approx = cv2.approxPolyDP(count, 0.1 * cv2.arcLength(count, True), True)
        if len(approx) == 5 :
            print "pentagon"
            cv2.drawContours(arg_image, [count], 0, (255, 0, 0), -1)
        elif len(approx) == 3 :
            print "triangle"
            cv2.drawContours(arg_image, [count], 0, (0, 255, 0), -1)
        elif len(approx) == 4 :
            print approx
            cv2.drawContours(arg_image, [count], 0, (0, 0, 255), -1)  # square
            for i in approx:
                x, y = i.ravel()
                cv2.circle(arg_image, (x, y), 1, (0, 255, 0), -1)

        elif len(approx) == 9 :
            print "half-circle"
            #cv2.drawContours(img, [count], 0, (255, 255, 0), -1)
        elif len(approx) > 15 :
            print "circle"
            #cv2.drawContours(img, [count], 0, (0, 255, 255), -1)

    return arg_image

# cv2.imwrite('data/r_detectshape.png', img)