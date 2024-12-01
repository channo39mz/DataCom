import socket

def start_tcp_server():
    # สร้าง socket object สำหรับ TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # กำหนด IP และพอร์ตของ server
    server_host = '0.0.0.0'  # ฟังบนทุก IP ที่เชื่อมต่อ
    server_port = 12345
    
    # ผูก socket กับที่อยู่และพอร์ต
    server_socket.bind((server_host, server_port))
    
    # ฟังการเชื่อมต่อเข้ามา
    server_socket.listen(1)

    # แสดง IP ของ server
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server กำลังฟังที่ {server_ip}:{server_port}")
    
    while True:
        # รอรับการเชื่อมต่อจาก client
        client_socket, client_address = server_socket.accept()
        print(f"ได้รับการเชื่อมต่อจาก {client_address}")
        
        # รับข้อมูลจาก client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        
        print(f"ข้อความที่ได้รับจาก client: {data}")
        
        # เปลี่ยนข้อความเป็นตัวใหญ่ทั้งหมด
        modified_data = data.upper()
        
        # ส่งข้อความกลับไปยัง client
        client_socket.send(modified_data.encode('utf-8'))
        
        # ปิดการเชื่อมต่อกับ client
        client_socket.close()

# เริ่ม server
start_tcp_server()
