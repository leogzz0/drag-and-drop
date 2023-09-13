import cv2
#import mediapipe
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)

# width and height
cap.set(3, 1280)
cap.set(4, 720)

# default is 0.5 but we want it to be harder to detect for better accuracy
detector = HandDetector(detectionCon=0.8)


while True:
    success, img = cap.read()
    #flip the image for better visualization
    img = cv2.flip(img, 1)
    # detection of hands in image
    img = detector.findHands(img)
    # detection of landmarks (fingers)
    lmList, _ = detector.findPosition(img)
    # default color
    colorRectangle = (255, 0, 255)
    # if our finger is in the rectangle
    if lmList:
        cursor = lmList[8]
        # check "x" and "y"
        if 100 < cursor [0] < 300 and 100 < cursor[1] < 300:
            # change color of the rectangle
            colorRectangle = 0, 255, 255
        else:
            colorRectangle = (255, 0, 255)


    cv2.rectangle(img, (100, 100), (300, 300), colorRectangle, cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
