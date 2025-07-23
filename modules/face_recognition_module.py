import cv2
import os
import numpy as np

STUDENT_IMAGES_DIR = "static/student_images/"
RECOGNIZER_PATH = "trainer.yml"

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

def capture_and_save_face(student_id):
    cam = cv2.VideoCapture(0)
    count = 0
    student_dir = os.path.join(STUDENT_IMAGES_DIR, str(student_id))
    os.makedirs(student_dir, exist_ok=True)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{student_dir}/{count}.jpg", face)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.imshow("Capture Faces", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27 or count >= 20:
            break

    cam.release()
    cv2.destroyAllWindows()
    train_recognizer()

def train_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = [], []

    for student_id in os.listdir(STUDENT_IMAGES_DIR):
        student_dir = os.path.join(STUDENT_IMAGES_DIR, student_id)
        if not os.path.isdir(student_dir):
            continue
        for img_name in os.listdir(student_dir):
            img_path = os.path.join(student_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            ids.append(int(student_id))

    recognizer.train(faces, np.array(ids))
    recognizer.save(RECOGNIZER_PATH)
    print("✅ Face recognizer trained and saved.")

def recognize_face_and_get_id():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(RECOGNIZER_PATH)

    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            student_id, confidence = recognizer.predict(face)
            print(f"Detected ID: {student_id}, Confidence: {confidence}")

            if confidence < 70:
                cam.release()
                cv2.destroyAllWindows()
                return str(student_id)

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

        cv2.putText(frame, "Press ESC to cancel", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Recognize Face", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
    return None
