﻿import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = "127.0.0.1"
PORT = 8001
BUFFER_SIZE = 1024
def handle_echo(addr,conn):
    print("Connected by", addr)
    full_data = conn.recv(BUFFER_SIZE)
            
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR) #shurdown thd socket
            
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address

        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            p = Process(target = handle_echo, args = (addr, conn))
            #p.daemon = True

            p.start()
            print("start Process",p)
            
            
            #recieve data, wait a bit, then send it back


            

if __name__ == "__main__":
    main()
