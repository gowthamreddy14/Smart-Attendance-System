
from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

TEMPLATE = '''
<!doctype html>
<title>Smart Attendance Dashboard</title>
<h1>Smart Attendance Dashboard</h1>
<table border=1>
  <tr><th>ID</th><th>Student ID</th><th>Date</th><th>Time</th><th>Status</th><th>Method</th></tr>
  {% for row in rows %}
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
'''

@app.route('/')
def show_attendance():
    conn = sqlite3.connect('attendance.db')
    rows = conn.execute("SELECT * FROM attendance").fetchall()
    conn.close()
    return render_template_string(TEMPLATE, rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
