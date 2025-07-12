
import sqlite3
import csv

conn = sqlite3.connect('attendance.db')
rows = conn.execute("SELECT * FROM attendance").fetchall()
with open('attendance_report.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'student_id', 'date', 'time', 'status', 'method'])
    writer.writerows(rows)
print("Exported to attendance_report.csv")
