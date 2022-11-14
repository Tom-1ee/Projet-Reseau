#!/usr/bin/python3

from platform import java_ver
from grid import *
from logging import exception
import socket

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect(("localhost", 7777))
        while True:
            data = s.recv(1024)
            if len(data) == 0:
                break
            data = data.decode()
            if ("<grid.grid object" in data):
                print(repr(grid(data)))
            else:
                print(data)
                shot = str(input (""))
                s.sendall(shot.encode())
           
        print("Connection closed.")
    except Exception as e:
        print("Connection proble : ", e)
main()