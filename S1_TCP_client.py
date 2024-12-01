from socket import *
serverName = '147.185.221.23'
serverPort = 12983
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print(f"Connected to server at {serverName}:{serverPort}")
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
print(f"Sent message: '{sentence}' to server at {serverName}:{serverPort}")
modifiedSentence = clientSocket.recv(1024)
print(f"Received response from server: '{modifiedSentence}' from {serverName}:{serverPort}")
print('From Server:', modifiedSentence.decode())
clientSocket.close()
