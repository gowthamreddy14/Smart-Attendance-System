import cv2
import os
import sqlite3

# ✅ Load Haar Cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# ✅ Open webcam
cap = cv2.VideoCapture(0)

# ✅ Get Student ID & Name
student_id = input("Enter Student ID: ")
name = input("Enter Student Name: ")

# ✅ Add student to students table
def add_student(student_id, name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    # Make sure students table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    # Insert student
    cursor.execute("INSERT OR IGNORE INTO students (student_id, name) VALUES (?, ?)", (student_id, name))
    conn.commit()
    conn.close()
    print(f"✅ Added '{name}' with ID {student_id} to students table!")

add_student(student_id, name)

# ✅ Create dataset folder if needed
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
        cv2.imwrite(f'dataset/User.{student_id}.{count}.png', face) # ✅ Use PNG if you want
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
    cv2.imshow('Face Capture', frame)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
        break

cap.release()
cv2.destroyAllWindows()
