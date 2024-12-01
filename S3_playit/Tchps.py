import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ระบุ URL และพอร์ตที่ได้จาก Playit.gg
playit_url = '147.185.221.22'
playit_port = 4069 

# รับ input จาก user
message = input("Enter message to send to server: ")
# ส่งข้อความไปยัง server
client_socket.sendto(message.encode(), (playit_url, playit_port))

# รับข้อความตอบกลับจาก server
response, server_address = client_socket.recvfrom(1024)
print(f"Received from server: {response.decode()}")

# ปิดการเชื่อมต่อ
client_socket.close()