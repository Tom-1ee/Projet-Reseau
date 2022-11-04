#!/usr/bin/python3

import socket

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 7777))
        while 1:
            data = s.recv(1024)
            if len(data) == 0:
                break
            print("Received:", repr(data))
        print("Connection closed.")
    except:
        print("ERROR")
main()