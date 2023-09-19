import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QSplashScreen
from PyQt5.QtCore import Qt
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # set properties for the start screen window
        self.setWindowTitle("Hand Tracker App")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(
            "background: #1FAEFF;"
            )
        #self.setStyleSheet("background-image: hand_indexes.png;")

        # create layout for the start screen
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # title label
        title_label = QLabel("Hand Tracker App")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 80px;"
            "font-weight: bold;"
            "color: white;"
            )

        # description label
        description_label = QLabel(
            "This application allows you to track your hands using advanced computer vision techniques. There would be 5 blocks to interact with. If you want to move them you should put your index finger and middle finger in peace sign on the block area, then you should join them to grab the block. Press 'Start' to begin, HAVE FUN!."
            )
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setWordWrap(True)
        description_label.setStyleSheet(
            "background-color: #0064BC;"
            "border-radius: 15px;"
            "font-size: 18px;" 
            "color: white;"
            )

        # create a "Start" button and connect it to the start_application method
        start_button = QPushButton("Start")
        # start_button.setAlignment(Qt.AlignCenter)
        start_button.setFixedSize(300, 50)
        start_button.setStyleSheet(
            "background-color: #FF9100;"
            "color: white;"
            "font-size: 20px;"
            "border-radius: 25px"
            )
        start_button.clicked.connect(self.start_application)

        # add widgets
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # set the layout for the start screen
        self.setLayout(layout)

    def start_application(self):
        # close the start screen
        self.close()

        # initialize the camera feed using OpenCV
        cap = cv2.VideoCapture(0)

        # width and height
        cap.set(3, 1280)
        cap.set(4, 720)

        # default is 0.5 but we want it to be harder to detect for better accuracy
        detector = HandDetector(detectionCon=0.8)
        # default color
        colorRectangle = (255, 0, 255)

        # class for multiple rectangle visualization
        class DragRect():
            def __init__(self, posCenter, size=[200, 200]):
                self.posCenter = posCenter
                self.size = size

            def update(self, cursor):
                cx, cy = self.posCenter
                w, h = self.size
                # check "x" and "y"
                # if the index finger tip is in the rectangle area
                if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
                    # change the position of the box
                    self.posCenter = cursor

        # create a list of DragRect objects (optimized) <-
        rectList = [DragRect([x * 250 + 150, 150]) for x in range(5)]

        while True:
            # read a frame from the camera feed
            success, img = cap.read()
            # flip the image for better visualization
            img = cv2.flip(img, 1)
            # detection fo hands in image
            img = detector.findHands(img)
            # detection of landmarks (fingers)
            lmList, _ = detector.findPosition(img)
            # if our finger is in the rectangle
            if lmList:
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                #print(l) #print help for visualization of length between index and middle finger
                if l < 30:
                    cursor = lmList[8] # index finger tip landmark (INDEX_FINGER_TIP)
                    # call the updated rectangle
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
                cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                              (cx + w // 2, cy + h // 2), colorRectangle, cv2.FILLED)
                cvzone.cornerRect(
                    imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
            out = img.copy()
            alpha = 0.5
            mask = imgNew.astype(bool)
            out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

            # display the modified frame
            cv2.imshow("Image", out)

            # exit the camera feed by pressing "q"
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release the camera and close camera feed
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # create a PyQt app
    app = QApplication(sys.argv)

    # create an instance of the StartScreen class and show it
    start_screen = StartScreen()
    start_screen.show()

    # Start the PyQt application event loop
    sys.exit(app.exec_())
