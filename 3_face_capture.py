                     
import cv2
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
student_id = input("Enter Student ID: ")
if not os.path.exists('dataset'):
    os.makedirs('dataset')
count = 0
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        count += 1
        face = frame[y:y+h, x:x+w]
        cv2.imwrite(f'dataset/User.{student_id}.{count}.jpg', face)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
    cv2.imshow('Face Capture', frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
        break
cap.release()
cv2.destroyAllWindows()
