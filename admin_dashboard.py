from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

# ✅ HTML template with auto-refresh
html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Smart Attendance Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        h2 { color: #333; }
        table { border-collapse: collapse; width: 100%; background: #fff; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #eee; }
    </style>
</head>
<body>
    <h2>📊 Smart Attendance — Admin Dashboard</h2>
    <p>This page auto-refreshes every 5 seconds to show new attendance records automatically.</p>
    <table>
        <tr>
            <th>Student ID</th>
            <th>Name</th>
            <th>Date</th>
            <th>Time</th>
            <th>Status</th>
            <th>Method</th>
        </tr>
        {% for row in records %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
            <td>{{ row[4] }}</td>
            <td>{{ row[5] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def dashboard():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # ✅ This JOIN shows only students who have marked attendance
    cursor.execute('''
        SELECT s.student_id, s.name, a.date, a.time, a.status, a.method
        FROM students s
        JOIN attendance a ON s.student_id = a.student_id
        ORDER BY a.date DESC, a.time DESC
    ''')

    records = cursor.fetchall()
    conn.close()

    return render_template_string(html, records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
