import cv2
import numpy as np
import face_recognition as fr
import os
import time
# import pyttsx3

# Initialize the text-to-speech engine
# engine = pyttsx3.init()


def findEncodings(images) :
    encodeList = list()
    for img in images :
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def faceReg(duration : int) :
    t = time.time()
    path = "/Users/anand/Documents/Sem5/Lab/IoT Lab/Project/HandTracker/FaceRecognition/Photos"
    images = list()
    classNames = list()
    myList = os.listdir(path)

    for cl in myList :
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])    
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True :
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = fr.face_locations(imgS)
        encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)
        name = "Unknown"
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame) :
            matches = fr.compare_faces(encodeListKnown, encodeFace)
            faceDis = fr.face_distance(encodeListKnown, encodeFace)
            matchInd = np.argmin(faceDis)
            if matches[matchInd] and faceDis[matchInd] < 0.5:
                name = classNames[matchInd].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        cv2.imshow('WebCam', img)
        cv2.waitKey(1)
        if int(time.time() - t) > duration :
            return name

if __name__ == "__main__" :
    print(faceReg(10))





