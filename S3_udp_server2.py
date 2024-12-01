import socket

def start_udp_server():
    # สร้าง socket object สำหรับ UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # กำหนด IP และพอร์ตของ server
    server_host = '0.0.0.0'  # ฟังบนทุก IP ที่เชื่อมต่อ
    server_port = 12345
    
    # ผูก socket กับที่อยู่และพอร์ต
    server_socket.bind((server_host, server_port))

    # แสดง IP ของ server
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"UDP Server กำลังฟังที่ {server_ip}:{server_port}")
    
    while True:
        # รับข้อมูลจาก client
        data, client_address = server_socket.recvfrom(1024)
        data = data.decode('utf-8')
        
        print(f"ได้รับข้อความจาก {client_address}: {data}")
        
        # เปลี่ยนข้อความเป็นตัวใหญ่ทั้งหมด
        modified_data = data.upper()
        
        # ส่งข้อความกลับไปยัง client
        server_socket.sendto(modified_data.encode('utf-8'), client_address)

# เริ่ม server
start_udp_server()
