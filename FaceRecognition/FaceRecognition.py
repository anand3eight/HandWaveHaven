import cv2
import numpy as np
import face_recognition as fr

imgElon = fr.load_image_file('/Users/anand/Documents/Sem5/Lab/IoT Lab/Project/FaceRecognition/Musk.jpeg')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
imgTest = fr.load_image_file('/Users/anand/Documents/Sem5/Lab/IoT Lab/Project/FaceRecognition/MuskTest.jpeg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

faceLoc = fr.face_locations(imgElon)[0]
encodeElon = fr.face_encodings(imgElon)[0]
cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

faceLocTest = fr.face_locations(imgTest)[0]
encodeTest = fr.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

results = fr.compare_faces([encodeElon], encodeTest)
faceDis = fr.face_distance([encodeElon], encodeTest)
cv2.putText(imgTest, f'{results} {round(faceDis[0], 2)}', (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

cv2.imshow("Elon Musk", imgElon)
cv2.imshow("Elon Test", imgTest)
cv2.waitKey(0)