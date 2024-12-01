import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = '192.168.100.45' 
server_port = 12000
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"TCP Server is listening on {server_ip}:{server_port}")

# รอการเชื่อมต่อจาก client
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

# รับข้อมูลจาก client
message = client_socket.recv(1024).decode()  
print(f"Received message: {message}")

# ส่งข้อความตอบกลับไปยัง client
response = message.upper()
client_socket.send(response.encode())

# ปิดการเชื่อมต่อ
client_socket.close()