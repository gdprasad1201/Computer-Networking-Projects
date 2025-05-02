from socket import *
import sys


serverPort = 6789
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))
serverSocket.listen(1)

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        
        if not message:
            connectionSocket.close()
            continue

        filename = message.split()[1][1:]

        if filename.endswith((".jpg", ".jpeg", ".JPEG")):
            f = open(filename, "rb")
            mode = "rb"
        else:
            f = open(filename, "r")
            mode = "r"
        
        outputdata = f.read()

        
        header = "HTTP/1.1 200 OK\r\n\r\n"
        connectionSocket.send(header.encode())

        if mode == "rb":
            connectionSocket.send(outputdata)
        else:
            connectionSocket.send(outputdata.encode())
        
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()

        
        
    except IOError:
        error_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        error_message = "<html><head></head><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(error_header.encode())
        connectionSocket.send(error_message.encode())
        
        connectionSocket.close()


serverSocket.close()
sys.exit(0)
