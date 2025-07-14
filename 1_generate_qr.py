
import sqlite3
import qrcode

# ✅ Ask for ID + Name
student_id = input("Enter Student ID: ")
name = input("Enter Student Name: ")

# ✅ Add student to students table
def add_student(student_id, name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO students (student_id, name) VALUES (?, ?)", (student_id, name))
    conn.commit()
    conn.close()
    print(f"✅ Added '{name}' with ID {student_id} to students table!")

add_student(student_id, name)

# ✅ Generate QR
qr = qrcode.make(student_id)
qr.save(f"QR_{student_id}.png")
print(f"✅ QR code saved as QR_{student_id}.png")
