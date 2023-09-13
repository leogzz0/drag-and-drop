import cv2
#import mediapipe
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
# width and height
cap.set(3, 1280)
cap.set(4, 720)
# default is 0.5 but we want it to be harder to detect for better accuracy
detector = HandDetector(detectionCon=0.8)
# default color
colorRectangle = (255, 0, 255)
# position values
cx, cy, w, h = 100, 100, 200, 200


while True:
    success, img = cap.read()
    #flip the image for better visualization
    img = cv2.flip(img, 1)
    # detection of hands in image
    img = detector.findHands(img)
    # detection of landmarks (fingers)
    lmList, _ = detector.findPosition(img)
    # if our finger is in the rectangle
    if lmList:
        l, _, _ = detector.findDistance(8, 12, img)
        #print(l)
        if l < 30:
            cursor = lmList[8]
            # check "x" and "y"
            if cx - w // 2 < cursor[0] < cy + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
                # change color of the rectangle
                colorRectangle = 0, 255, 255
                cx, cy = cursor
            else:
                colorRectangle = (255, 0, 255)

    cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorRectangle, cv2.FILLED)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
