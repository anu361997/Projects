import numpy as np 
import cv2
import os
 
import Face_Detection as fr 

test_img = cv2.imread(r'/home/anamika/Desktop/test_image.jpg')

faces_detected,gray_img = fr.faceDetection(test_img)
#print(len(faces_detected))

print("Face Detected ",faces_detected)

#training will begin from here

faces,face_ID = fr.labels_for_training_data(r'/home/anamika/Desktop/Face_Detection/images')
face_recognizer = fr.train_classifier(faces,face_ID)
face_recognizer.save(r'/home/anamika/Desktop/Face_Detection/trainingdata.yml')

name ={0:'Anamika',1:'Ian Somarhalder'}

for face in faces_detected:
    (x,y,w,h)=face
    roi_gray=gray_img[y:y+h,x:x+w]
    label,confidence = face_recognizer.predict(roi_gray)
    print(label)
    print(confidence) 
    fr.draw_rect(test_img,face)
    predict_name=name[label]
    fr.put_text(test_img,predict_name,x,y)

resized_image = cv2.resize(test_img,(1000,1000))
cv2.imshow('resized_image: ' , resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows
