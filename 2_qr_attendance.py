
import cv2
import sqlite3
from datetime import datetime

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

conn = sqlite3.connect('attendance.db')
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
conn.commit()

while True:
    _, frame = cap.read()
    data, bbox, _ = detector.detectAndDecode(frame)
    if data:
        now = datetime.now()
        date, time_now = now.strftime('%Y-%m-%d'), now.strftime('%H:%M:%S')
        status = "On Time" if time_now <= "09:15:00" else "Late"
        conn.execute('INSERT INTO attendance (student_id, date, time, status, method) VALUES (?, ?, ?, ?, ?)',
                     (data, date, time_now, status, 'QR Code'))
        conn.commit()
        print(f"Attendance marked for {data} ({status})")
    cv2.imshow("QR Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()
