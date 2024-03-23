import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui as pg

wCam, hCam = 640, 480
frameRed = 100
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)
wScr, hScr = pg.size()
print(wScr, hScr)



while True :
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    cv2.rectangle(img, (frameRed, frameRed), (wCam - frameRed, hCam - frameRed), (255, 0, 255), 2)
    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0 :
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        # 4. Only Index Finger : Hover mode
        if fingers[1] == 1 and fingers[2] == 0 :
            
            # 5. Convert Co-Ordinates
            x3 = np.interp(x1, (0, wCam-frameRed), (0, wScr))
            y3 = np.interp(y1, (0, hCam-frameRed), (0, hScr))
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move the Mouse
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            pg.moveTo(wScr - clocX, clocY)
            plocX, plocY = clocX, clocY
        # 8. Both Index and Middle fingers are up : Clicking Mode
        elif fingers[1] == 1 and fingers[2] == 1 :
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)

            # 10. Click mouse if distance is lesser than threshold
            if length <= 30 :
                cv2.circle(img, (lineInfo[-2], lineInfo[-1]), 15, (0, 255, 0), cv2.FILLED)
                pg.click()
        # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS : {int(fps)}", (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)