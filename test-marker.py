import socket
import struct
import time

# กำหนดที่อยู่ IP และพอร์ตของ OpenBCI GUI
ip_address = '127.0.0.1'  # หรือ IP ของเครื่องที่เปิด OpenBCI GUI
port = 12345  # พอร์ตที่กำหนดใน OpenBCI GUI

# สร้าง socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ส่ง marker ทุก 5 วินาที
marker_count = 0
while True:
    # แปลงตัวเลขเป็น binary data และส่งผ่าน socket UDP
    # marker_data = struct.pack('!i', marker_count)  # !i หมายถึง integer ในรูปแบบ big-endian
    # print(marker_data)
    sock.sendto(b'E000', (ip_address, port))
    print("Marker", marker_count, "sent.")
    
    marker_count += 1
    time.sleep(5)
