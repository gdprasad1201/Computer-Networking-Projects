#import socket module
from socket import *
import sys # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverPort = 8080
serverSocket.bind(('localhost', serverPort)) 
serverSocket.listen(1) #wait and listen for some client to knock on the door

while True:
	# Establish the connection
	print('The server is ready to serve...')
	connectionSocket, addr = serverSocket.accept() #the server creates a new socket dedicated to the particular client

	try:
		message = connectionSocket.recv(1024) #receives message from client
		print("The message is: ", message)
		
		filename = message.split()[1]
		print("The filename is: ", filename)

		# if file is image
		if filename.decode().endswith(".jpg") or filename.decode().endswith(".jpeg") or filename.decode().endswith(".png") or filename.decode().endswith(".gif"):
			f = open(filename[1:], 'rb')
		else:
			f = open(filename[1:]) #get rid of '/' in the front of the filename
		outputdata = f.read() #read the file
		
		#Send one HTTP header line into socket
		connectionSocket.send("\nHTTP/1.1 200 OK\r\n\r\n".encode())
		
		#Send the content of the requested file to the client
		print("The length of the outputdata is: ", len(outputdata))
		
		if filename.decode().endswith(".jpg") or filename.decode().endswith(".jpeg") or filename.decode().endswith(".png") or filename.decode().endswith(".gif"):
			connectionSocket.send(outputdata)
		else:
			for i in range(len(outputdata)):
				connectionSocket.send(outputdata[i].encode())

		connectionSocket.send("\r\n".encode()) 
		
		print('File sending success')
		connectionSocket.close()
	except IOError:
		#Send response message for file not found
		connectionSocket.send("\nHTTP/1.1 404 Not Found\r\n\r\n".encode())
		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

		#Close client socket
		connectionSocket.close() 
		
serverSocket.close() #Close the server socket
sys.exit() #Terminate the program after sending the corresponding data