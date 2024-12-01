from socket import *
serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The TCP server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    modifiedSentence = sentence.upper()
    print(modifiedSentence)
    connectionSocket.send(modifiedSentence.encode())
    connectionSocket.close()
