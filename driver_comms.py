
import socket                

s = socket.socket()          
port = 12345     # Reserve a port on your computer...in our case it is 12345, but it can be anything
s.bind(('', port))         
s.listen(5)    # Put the socket into listening mode    

conn_established = False

while True:
  c, addr = s.accept()   # Establish connection with client
  if not conn_established:
    print ('Engineer Connected: ', addr)
    conn_established = True  
  
  DC = input("Driver Comms: ")
  c.send(DC.encode('utf-8'))   # Send a message to the client
  