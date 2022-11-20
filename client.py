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

                #split the string in order to get datas per cells
                x = data.split("[")
                y = x[1].split("]")
                my_cell = y[0].split(",")

                for i in range(3):
                    print("|",symbols[int(my_cell[i*3])], "|",  symbols[int(my_cell[i*3+1])], "|",  symbols[int(my_cell[i*3+2])], "|");
                    print("-------------")

            elif("quelle case" in data):
                shot = str(input (data))
                s.sendall(shot.encode())
            elif("Quel mode" in data):
                mode = str(input(data))
                s.sendall(mode.encode())
            elif("END" in data):
                print("La partie est terminée, vous pouvez quitter en pressant Ctrl+C")
            else:
                print(data)
                
           
        print("Connection closed.")
    except Exception as e:
        print("[ManMade Error] Disconnected because : ", e)
main()