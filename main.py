import cv2
#import mediapipe
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

# start screen backgorund
start_screen = np.zeros((720, 1280, 3), dtype=np.uint8)

# text instructions
font = cv2.FONT_HERSHEY_SIMPLEX
text = "Click Any Key to Start"
text_size = cv2.getTextSize(text, font, 2, 5)[0]
text_x = (start_screen.shape[1] - text_size[0]) // 2
text_y = (start_screen.shape[0] + text_size[1]) // 2
cv2.putText(start_screen, text, (text_x, text_y),
            font, 2, (255, 255, 255), 5, cv2.LINE_AA)

# display the start screen
cv2.imshow("Start Screen", start_screen)
cv2.waitKey(0)
cv2.destroyAllWindows()

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

# class for multiple rectangle visualization
class DragRect():
    # initialization
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size
    
    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        # check "x" and "y"
        # if the index finger tip is in the rectangle area
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            # change color of the rectangle
            # colorRectangle = 0, 255, 255
            # change the position of the box
            self.posCenter = cursor   

rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

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
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        #print(l)
        if l < 30:
            cursor = lmList[8] # index finger tip landmark
            # call the update here
            for rect in rectList:
                rect.update(cursor)

    ## Draw solid
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorRectangle, cv2.FILLED)
    #     cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    ## Draw Transparency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorRectangle, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha , 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)
