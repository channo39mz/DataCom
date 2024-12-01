from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
server_name = gethostname()
server_ip = gethostbyname(server_name)
print(server_name , server_ip)
print('The UDP server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    print(modifiedMessage)
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
