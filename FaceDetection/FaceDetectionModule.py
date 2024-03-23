import cv2
import mediapipe as mp
import time

class FaceDetector :
    def __init__(self, 
                 minDetectionCon = 0.5) :
        
        self.minDetectionCon = minDetectionCon

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw=True) :
        bBoxes = list()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        if self.results.detections :
            for id, detection in enumerate(self.results.detections) :
                bBoxC = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bBox = int(bBoxC.xmin * w), int(bBoxC.ymin * h), int(bBoxC.width * w), int(bBoxC.height * h)
                bBoxes.append([id, bBox, detection.score])
                if draw : 
                    img = self.fancyDraw(img, bBox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bBox[0], bBox[1]-20), cv2.FONT_HERSHEY_PLAIN, 3, (255,0, 255), 2)
        return img, bBoxes

    def fancyDraw(self, img, bBox, l=30, t=10, rt=1) :
        x, y, w, h = bBox
        x1, y1 = x + w, y + h
        cv2.rectangle(img, bBox, (255, 0, 255), rt)
        # Top Left : x, y
        cv2.line(img, (x, y), (x+l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y+l), (255, 0, 255), t)

        # Top Right : x1, y
        cv2.line(img, (x1, y), (x1-l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y+l), (255, 0, 255), t)

        # Bottom Left : x, y1
        cv2.line(img, (x, y1), (x+l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1-l), (255, 0, 255), t)

        # Top Right : x1, y1
        cv2.line(img, (x1, y1), (x1-l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1-l), (255, 0, 255), t)
        return img

def main() :
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    while True :
        success, img = cap.read()
        img, bBoxes = detector.findFaces(img)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS : {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 2)
        cv2.waitKey(1)
        cv2.imshow("Image", img)

if __name__ == '__main__' :
    main()