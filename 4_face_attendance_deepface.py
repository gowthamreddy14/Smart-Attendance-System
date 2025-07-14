import cv2
import os
import sqlite3
from datetime import datetime
import pyttsx3
from deepface import DeepFace

# Initialize TTS engine
engine = pyttsx3.init()

# Initialize SQLite (with error handling)
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect('attendance.db', timeout=10) # Prevents DB locks
        return conn
    except sqlite3.Error as e:
        print(f"[SQLite Error] {e}")
        return None

# Create tables if they don't exist
def init_db():
    conn = get_db_connection()
    if conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                date TEXT,
                time TEXT,
                status TEXT,
                method TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leave_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                date TEXT
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# Initialize camera
cap = cv2.VideoCapture(0)
marked_today = set()
dataset_path = "dataset"
print("[INFO] Running DeepFace Attendance...")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to capture frame")
        break

    img_path = "live_frame.jpg"
    cv2.imwrite(img_path, frame)

    try:
        # Debug: Check if face is detected
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            print("[DEBUG] No face detected in frame")
            cv2.imshow("DeepFace Attendance", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        print("[DEBUG] Face detected, running DeepFace...")
        dfs = DeepFace.find(
            img_path=img_path,
            db_path=dataset_path,
            model_name='Facenet',
            enforce_detection=False,
            detector_backend='opencv'
        )
        
        if dfs and not dfs[0].empty:
            student_file = dfs[0]['identity'].iloc[0]
            student_id = os.path.splitext(os.path.basename(student_file))[0].split('.')[1]
            print(f"[DEBUG] Recognized Student ID: {student_id}")

            today = datetime.now().strftime('%Y-%m-%d')
            conn = get_db_connection()
            if conn:
                cursor = conn.execute('SELECT * FROM leave_table WHERE student_id=? AND date=?', (student_id, today))
                if cursor.fetchone():
                    print(f"[INFO] Student {student_id} is on leave today.")
                    conn.close()
                    continue

                if student_id not in marked_today:
                    now = datetime.now()
                    time_now = now.strftime('%H:%M:%S')
                    status = "On Time" if time_now <= "09:30:00"  else "Late"

                    
                    conn.execute('INSERT INTO attendance (student_id, date, time, status, method) VALUES (?, ?, ?, ?, ?)',
                                (student_id, today, time_now, status, 'DeepFace'))
                    conn.commit()
                    marked_today.add(student_id)
                    print(f"[SUCCESS] Marked {student_id} at {time_now} ({status})") # <-- This should appear in terminal
                    engine.say(f"Welcome {student_id}")
                    engine.runAndWait()
                conn.close()
        else:
            print("[DEBUG] No matching face in database")

    except Exception as e:
        print(f"[ERROR] {str(e)}")

    cv2.imshow("DeepFace Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
