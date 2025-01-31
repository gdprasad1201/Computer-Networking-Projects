"""
Currently, the web server handles only one HTTP request at a time. Implement a multithreaded server 
that is capable of serving multiple requests simultaneously. Using threading, first create a main thread 
in  which  your  modified  server  listens  for  clients  at  a  fixed  port.  When  it  receives  a  TCP  connection 
request  from  a  client,  it  will  set  up  the  TCP  connection  through  another  port  and  services  the  client 
request  in  a  separate  thread.  There  will  be  a  separate  TCP  connection  in  a  separate  thread  for  each 
request/response pair.
"""

from socket import *
import sys
import threading
import datetime

def handle_client(connectionSocket, addr):
    try:
        message = connectionSocket.recv(1024) #receives message from client
        print( '-------the message is------- ', message)
        
        filename = message.split()[1]
        print('-------the filename is------ ', filename )
        f = open(filename[1:]) #get rid of '/' in the front of the filename
        outputdata = f.read()
        
        #Send one HTTP header line into socket
        # a bytes-like object is required, not 'str'
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        
        #Send the content of the requested file to the client
        
        print('-------length is------ ', len(outputdata))
        for i in range(len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            
        connectionSocket.send("\r\n".encode()) 
        
        print('File sending success')
    except IOError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        #Close client socket
        connectionSocket.close() 
    except IndexError:
        #Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        #Close client socket
        connectionSocket.close()
        
    serverSocket.close() #Close the server socket
    sys.exit() #Terminate the program after sending the corresponding data

serverSocket = socket(AF_INET, SOCK_STREAM)

#Prepare a sever socket
serverPort = 8080
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1) #wait and listen for some client to knock on the door

while True:
    #Establish the connection
    print('The server is ready to serve...')
    connectionSocket, addr = serverSocket.accept() #the server creates a new socket dedicated to the particular client
    print('Connection from: ', addr)
    threading.Thread(target=handle_client, args=(connectionSocket, addr)).start()
    #handle_client(connectionSocket, addr)
    #connectionSocket.close() #close the connection after handling the client request
    #print('Connection closed')

serverSocket.close() #Close the server socket
sys.exit() #Terminate the program after sending the corresponding data
