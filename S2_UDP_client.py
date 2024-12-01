from socket import *
serverName = '192.168.192.243'  # เปลี่ยนเป็น localhost
serverPort = 13000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print('From Server:', modifiedMessage.decode())
clientSocket.close()