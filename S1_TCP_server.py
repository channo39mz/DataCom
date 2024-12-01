from socket import *
serverPort = 9917
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print(f"Server is running on port {serverPort}")

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    print(f"Received message: {sentence} from {addr[0]}:{addr[1]}")
    modifiedSentence = sentence.upper()
    print(modifiedSentence)
    connectionSocket.send(modifiedSentence.encode())
    print(f"Sent response: {modifiedSentence} to {addr[0]}:{addr[1]}")
    connectionSocket.close()
