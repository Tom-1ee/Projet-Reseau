#!/usr/bin/python3

from platform import java_ver
from grid import *
from logging import exception
import socket
import time
def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostname = socket.gethostname()
        s.connect(("localhost", 7777))
        while True:
            data = s.recv(1024)
            if len(data) == 0:
                time.sleep(0.1)
            data = data.decode()
            if ("<class 'grid.grid'" in data):
                #for i in range(3):
                    #print("|",symbols[i*3], "|",  symbols[i*3+1], "|",  symbols[i*3+2], "|");
                #data = repr(grid(data))
                #print(data.cells)
                print(data)

            elif("quelle case" in data):
                shot = str(input (data))
                s.sendall(shot.encode())
            elif("Quel mode" in data):
                mode = str(input(data))
                s.sendall(mode.encode())
            elif("END" in data):
                break
            else:
                print(data)
                
           
        print("Connection closed.")
    except Exception as e:
        print("[ManMade Error] Disconnected because : ", e)
main()