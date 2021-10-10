import numpy as np
import cv2
import os

import Face_Detection as fr
print (fr)

test_img=cv2.imread(r'/home/anamika/Desktop/test_image2.jpg')      #Give path to the image which you want to test


faces_detected,gray_img=fr.faceDetection(test_img)
print("face Detected: ",faces_detected)


face_recognizer=cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read(r'/home/anamika/Desktop/Face_Detection/trainingdata.yml')  #Give path of where trainingData.yml is saved

name={0:"Anamika",1:"Ian Somerhalder"}             #Change names accordingly.  If you want to recognize only one person then write:- name={0:"name"} thats all. Dont write for id number 1. 

for face in faces_detected:
    (x,y,w,h)=face
    roi_gray=gray_img[y:y+h,x:x+h]
    label,confidence=face_recognizer.predict(roi_gray)
    print ("Confidence :",confidence)
    print("label :",label)
    fr.draw_rect(test_img,face)
    predicted_name=name[label]
    if(confidence>47):
        fr.put_text(test_img,"Unknown",x,y)
        continue
    fr.put_text(test_img,predicted_name,x,y)

resized_img=cv2.resize(test_img,(1000,700))

cv2.imshow("face detection ", resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows