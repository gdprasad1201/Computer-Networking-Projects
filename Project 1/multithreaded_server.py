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

class ClientThread(threading.Thread):
    def __init__(self, connectionSocket, addr):
        threading.Thread.__init__(self)
        self.connectionSocket = connectionSocket
        self.addr = addr
        print('New connection added: ', addr)

    def run(self):
        while True:
            try:
                message = self.connectionSocket.recv(1024)
                print('-------the message is------- ', message)

                filename = message.split()[1]
                print('-------the filename is------ ', filename)

                f = open(filename[1:]) #get rid of '/' in the front of the filename
                outputdata = f.read()

                self.connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
                for i in range(len(outputdata)):
                    self.connectionSocket.send(outputdata[i].encode())
                self.connectionSocket.send("\r\n".encode()) 
                self.connectionSocket.close() 

                print('File sending success')
            except IOError:
                self.connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                self.connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
                self.connectionSocket.close()
            except IndexError:
                self.connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                self.connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
                self.connectionSocket.close()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8080
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)
threads = []

while True:
    print('The server is ready to serve...')

    connectionSocket, addr = serverSocket.accept()

    newThread = ClientThread(connectionSocket, addr)
    newThread.start()

    threads.append(newThread)

for t in threads:
    t.join()

serverSocket.close()
sys.exit()