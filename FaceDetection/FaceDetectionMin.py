import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
pTime = 0

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(0.75)


while True :
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    if results.detections :
        for id, detection in enumerate(results.detections) :
            bBoxC = detection.location_data.relative_bounding_box
            h, w, c = img.shape
            bBox = int(bBoxC.xmin * w), int(bBoxC.ymin * h), int(bBoxC.width * w), int(bBoxC.height * h)
            cv2.rectangle(img, bBox, (255, 0, 255), 2)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bBox[0], bBox[1]-20), cv2.FONT_HERSHEY_PLAIN, 3, (255,0, 255), 2)
            # mpDraw.draw_detection(img, detection)
     
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 2)
    cv2.waitKey(1)
    cv2.imshow("Image", img)