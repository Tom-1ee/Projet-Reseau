#!/usr/bin/python3

import socket

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    # LE PROBLEME ET LA, DANS LE CONNECT.
        s.connect((ip_address, 7777))

        s.sendall("TEST")
        while True:
            data = s.recv(1024)
            if len(data) == 0:
                break
            print("Received:", data)
        print("Connection closed.")
    except:
        print("ERROR")
main()