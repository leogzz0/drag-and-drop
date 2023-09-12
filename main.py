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
    # detection of hands in image
    img = detector.findHands(img)
    # detection of landmarks (fingers)
    lmList, _ = detector.findPosition(img)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
