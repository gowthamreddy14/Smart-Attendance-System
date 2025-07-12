
import qrcode

student_id = input("Enter Student ID: ")
qr = qrcode.make(student_id)
qr.save(f"QR_{student_id}.png")
print(f"QR code saved as QR_{student_id}.png")
