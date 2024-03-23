import cv2
import time 
import os
import HandTrackingModule as htm
import VolumeControl as vc
import Arduino as ard
from FaceRecognition import AttendanceSystem as ats
import sensor as se
from gtts import gTTS
import serial

ser = serial.Serial('/dev/cu.usbmodem11301', 9600, timeout=1)

def speak(text) :
    speech = gTTS(text)
    speech_file = 'speech.mp3'
    speech.save(speech_file)
    os.system('afplay ' + speech_file)


wCam, hCam = 1080, 720
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "HandTracker/Photos"
myList = sorted(os.listdir(folderPath))
print(myList)
overlayList = []
for imPath in myList :
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
prevLs = list()

while True :
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0 :
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1] :
            fingers.append(1)
        else :
            fingers.append(0)

        # Four Fingers
        for id in range(1, 5) :
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-3][2] :
                fingers.append(1)
            else :
                fingers.append(0)
        totalFingers = fingers.count(1)
        print(totalFingers)
        prevLs.append(totalFingers)
        if prevLs[-1:max(-len(prevLs), -11):-1].count(0) >= 10 and totalFingers == 0 :
            # Off Command
            print('Off') 
            speak('Switching Off Devices')
            se.off(ser)
        elif prevLs[-1:max(-len(prevLs), -11):-1].count(1) >= 10 and totalFingers == 1 :
            cv2.waitKey(10)
            print('Controlling Volumne') 
            speak('Controlling Volume')
            vc.volumeControl() 
        elif prevLs[-1:max(-len(prevLs), -11):-1].count(2) >= 10 and totalFingers == 2 :
            cv2.waitKey(10)
            print('Switching On LED') 
            speak('Switching On LED')
            se.led(ser)
        # elif prevLs[-1:max(-len(prevLs), -11):-1].count(3) >= 10 and totalFingers == 3 :
        #     cv2.waitKey(10)
        #     print('Switching On Buzzer') 
        #     speak('Switching On Buzzer')
        #     se.buzzer(ser)
        elif prevLs[-1:max(-len(prevLs), -11):-1].count(3) >= 10 and totalFingers == 3 :
            cv2.waitKey(10)
            print('Checking Temperature')
            speak('Checking Temperature')
            val = se.tempCheck(ser)
            if val is not None :
                speak(f'Temperature is currently {val} degree celsius')
            else :
                speak(f'Could not get the temperature')
        elif prevLs[-1:max(-len(prevLs), -11):-1].count(4) >= 10 and totalFingers == 4 :
            cv2.waitKey(10)
            speak('Recognizing Faces')
            speak(ats.faceReg(5))
        prev = totalFingers        
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(10)
