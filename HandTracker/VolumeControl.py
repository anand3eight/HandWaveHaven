import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript


def volumeControl() :
    wCam, hCam = 640, 480
    minVol, maxVol = 0, 100
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, wCam)
    pTime = 0
    vol, volBar, volPct = 0, 400, 0

    detector = htm.handDetector(detectionCon = 0.7, maxHands=1)
    while True :
        success, img = cap.read()
        img = detector.findHands(img, draw=False)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0 :
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            length, img, lineInfo = detector.findDistance(8, 12, img, draw=False)
            if(length <= 30) :
                break
            cx, cy = (x1+x2)//2, (y1+y2)//2
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            length = math.hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPct = np.interp(length, [50, 300], [0, 100])
            osascript.osascript(f"set volume output volume {vol}")
            if length < 50 :
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f"{int(volPct)}%", (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS : {(int(fps))}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__' :
    volumeControl()