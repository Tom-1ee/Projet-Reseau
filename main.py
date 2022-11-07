#!/usr/bin/python3

from grid import *
import  random
from pickle import NONE
import sys 
import socket
import select

def main():


    serv = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(("", 7777))
    serv.listen(1)
    clients = {serv:"serveur"}
    sockets,l1,l2 = [serv],[],[]
    nicknames = ["serv"]

    while True:
        reader, writer, error = select.select(sockets,l1,l2)
        for x in reader:
            if x == serv:
                sc, a = serv.accept()
                nickname = str(sc.getpeername()) #gives out nickname
                clients[sc] = nickname #gives a name to the socket
                print("client connected : ", nickname)
                for other in clients:
                    name_self = clients[sc]
                    if other != sc and other != serv: #don't send message to self nor to server #SEND message to everyone about the new client who connected 
                        other.send("client connected : ".encode() + name_self.encode() + " \n".encode())
                    else:
                        None
                    try:
                         msg = x.recv(1500)
                    except:
                        None

    grids = [grid(), grid(), grid()]
    current_player = J1
    grids[J1].display()
    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("quel case allez-vous jouer ?"))
            current_player = J2
        else:
            shot = random.randint(0,8)
            while grids[current_player].cells[shot] != EMPTY:
                shot = random.randint(0,8)
            current_player = J1
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
        if current_player == J1:
            grids[J1].display()
    print("game over")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print("You win !") 
    else:
        print("you loose !")

main()
