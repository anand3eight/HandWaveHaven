import cv2
import mediapipe as mp
import time

class FashMeshDetector :
    def __init__(self, 
                 staticMode = False, 
                 maxFaces = 2,
                 minDetectionCon = 0.5,
                 minTrackCon = 0.5) :
        
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxFaces, False, self.minDetectionCon, self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=2, circle_radius=2)

    def findFaceMesh(self, img, draw = True): 
        faces = list()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)
        if self.results.multi_face_landmarks :
            for faceLms in self.results.multi_face_landmarks :
                face = list()
                if draw :
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)
                for id, lm in enumerate(faceLms.landmark) :
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    face.append([id, x, y])
                faces.append(face)
        return img, faces

def main() :
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FashMeshDetector()
    while True :
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img, False)
        if len(faces) != 0 :
            print(faces)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS : {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__' :
    main()