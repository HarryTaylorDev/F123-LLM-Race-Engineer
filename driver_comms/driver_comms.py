
import socket
import time           

s = socket.socket()          
port = 12345
s.bind(('', port))         
s.listen(5)    # Put the socket into listening mode    
print("Listening for engineer client response...")

conn_established = False

while True:
  c, addr = s.accept()   # Establish connection with client
  if not conn_established:
    print ('Engineer Connected: ', addr)
    conn_established = True  
    time.sleep(3)
    driver_name = input("Input Driver Name: ")
    driver_name = "_dn_ Your Driver is: "+driver_name 
    c.send(driver_name.encode('utf-8'))
    break

while True:
  c, addr = s.accept()   # Establish connection with client

  DC = input("Driver Comms Input: ")
  c.send(DC.encode('utf-8'))   # Send a message to the client
  