#!/usr/bin/python3

from logging import exception
import socket

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect(("localhost", 7777))

        s.sendall("TEST".encode())
        while True:
            data = s.recv(1024)
            if len(data) == 0:
                break
            print("Received:", data)
        print("Connection closed.")
    except Exception as e:
        print("Connection proble : ", e)
main()