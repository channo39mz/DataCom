from socket import *
serverName = 'localhost'  # เปลี่ยนเป็น localhost
serverPort = 19006
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print('From Server:', modifiedMessage.decode())
clientSocket.close()
