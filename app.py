from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from modules import face_recognition_module as frm
import pandas as pd
from datetime import datetime

app = Flask(__name__)
DB = 'database.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                class TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                date TEXT,
                time TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')

        c.execute("SELECT COUNT(*) FROM admins")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO admins (username, password) VALUES (?, ?)", ('admin', '14201'))


init_db()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/student_login', methods=['POST'])
def student_login():
    return render_template('student_dashboard.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()

    if result:
        return render_template('admin_dashboard.html')
    else:
        return "❌ Invalid admin username or password!"

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        student_id = int(request.form['id']) # Force numeric ID for LBPH!
        name = request.form['name']
        class_name = request.form['class']

        with sqlite3.connect(DB) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO students (id, name, class) VALUES (?, ?, ?)",
                      (student_id, name, class_name))

        frm.capture_and_save_face(student_id)
        return redirect(url_for('admin_dashboard'))
    return render_template('register_student.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/mark_attendance')
def mark_attendance():
    student_id = frm.recognize_face_and_get_id()
    if student_id:
        now = datetime.now()
        date_value = now.strftime('%Y-%m-%d') # ✅ convert to string
        time_value = now.strftime('%H:%M:%S') # ✅ convert to string

        with sqlite3.connect(DB) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)",
                      (int(student_id), date_value, time_value))
            c.execute("SELECT name FROM students WHERE id = ?", (student_id,))
            name = c.fetchone()[0]

        return render_template('attendance_success.html',
                               name=name, date=date_value, time=time_value)
    else:
        return "Face not recognized! Try again."

@app.route('/remove_student', methods=['GET', 'POST'])
def remove_student():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        if request.method == 'POST':
            student_id = int(request.form['id'])
            c.execute("DELETE FROM students WHERE id = ?", (student_id,))
        c.execute("SELECT * FROM students")
        students = c.fetchall()
    return render_template('remove_student.html', students=students)

@app.route('/attendance_report')
def attendance_report():
    with sqlite3.connect(DB) as conn:
        df = pd.read_sql_query("SELECT * FROM attendance", conn)
        if not df.empty:
            daily = df.groupby(['student_id', 'date']).size().reset_index(name='count')
            daily.to_excel('daily_attendance.xlsx', index=False)

            df_students = pd.read_sql_query("SELECT * FROM students", conn)
            df = df.merge(df_students, left_on='student_id', right_on='id')
            df['month'] = pd.to_datetime(df['date']).dt.month
            monthly = df.groupby(['class', 'month'])['student_id'].nunique().reset_index(name='students_present')
            monthly.to_excel('monthly_attendance.xlsx', index=False)
    return render_template('attendance_report.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
