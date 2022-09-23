#!/usr/bin/env python3
import socket
import time
import sys
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#127.0.0.1 
def get_remote_ip(host):
    print(f'getting ip for {host}')
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Host name can not be resolved')
        sys.exit()
    print(f'IP address of {host} is {remote_ip}')
    return remote_ip


def main():

    host = 'www.google.com'
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print('starting your proxy server')
        
        
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode

        proxy_start.listen(2)
        
       
        #continuously listen for connections
        while True:
            connection, address = proxy_start.accept()
            print("Connected by", address)
            # create a new socket.,+++++=
            processBegin = Process(target = handle, args = (connection,address))
            processBegin.start()
            

def dataHandle(connection):
    information = b""
    while True:
        f_data = connection.recv(BUFFER_SIZE)
        if not f_data:
            break
        information = information + f_data

    return information
    

def handle(connection,address):

        full_data = dataHandle(connection)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
            proxy_end.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #recieve data, wait a bit, then send it back

            print('connecting to google')
            proxy_end.settimeout(1)
            remote_ip = get_remote_ip("www.google.com")
            #connect to the end
           
            proxy_end.connect((remote_ip,80))

            proxy_end.sendall(full_data)
            
            googleR = b""
            while True:
                data = proxy_end.recv(BUFFER_SIZE)
                if not data:
                    break

                googleR = googleR + data

            connection.sendall(googleR)
            connection.shutdown(socket.SHUT_RDWR)

        connection.close()

if __name__ == "__main__":
    main()

