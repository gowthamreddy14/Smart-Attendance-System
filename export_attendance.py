import sqlite3
import csv

# ✅ Connect to the DB
conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# ✅ Get only needed columns
cursor.execute('''
    SELECT student_id, date, time, status, method
    FROM attendance
    ORDER BY date DESC
''')

rows = cursor.fetchall()
conn.close()

# ✅ Export to CSV
with open('attendance_report.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Student ID', 'Date', 'Time', 'Status', 'Method'])
    writer.writerows(rows)

print("✅ Exported to attendance_report.csv!")
