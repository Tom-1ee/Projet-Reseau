#!/usr/bin/python3

from platform import java_ver
from grid import *
import  random
from pickle import NONE
import sys 
import socket
import select
import time

def main():

    Joueur1 = "noone"
    Joueur2 = "noone"
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
                if Joueur1 != "noone":  #avant ça, regarder le nombre de joueurs
                    Joueur2 = nickname
                else:
                    Joueur1 = nickname
                clients[nickname] = sc #gives a name to the socket
                print("client connected : ", nickname)
                nicknames.append(nickname)
                for other in clients:
                    name_self = clients[nickname]
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
                    clients[nicknames[1]].sendall(str(grids[J1]).encode())
                    #grids[J1].display()
                    while grids[0].gameOver() == -1:
                        if current_player == J1:
                            shot = -1
                            while shot <0 or shot >=NB_CELLS:
                               clients[nicknames[1]].sendall("quelle case allez-vous jouer ?".encode())
                               data = "no"
                               while (type(data) != int):
                                    time.sleep(0.5)
                                    print(type(data))
                                    data = clients[nicknames[1]].recv(1500).decode()
                                    try:
                                        data = int(data)
                                    except:
                                        print("OULALA PEUT PAS INT CA")
                               shot = data
                               grids[0].display()
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
                            None
                            #grids[J1].display()
                    print("game over")
                    grids[0].display()
                    if grids[0].gameOver() == J1:
                        print("You win !") 
                    else:
                        print("you loose !")

main()
