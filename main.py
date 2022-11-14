#!/usr/bin/python3

from platform import java_ver
from grid import *
import  random
from pickle import NONE
import sys 
import socket
import select
import time
import os
import threading


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


################################################################################################################
### TANT QUE len(nicknames) PAS SUPERIEUR A 3 OU QUE LE MODE CHOISIS EST PAS "SOLO" ON CONTINUE LA RECHERCHE ###
################################################################################################################
    while True:
            reader, writer, error = select.select(sockets,l1,l2)
            for x in reader:
                if x == serv:
                    sc, a = serv.accept()
                    nickname = str(sc.getpeername()) #gives out nickname
                    if Joueur1 != "noone": 
                        Joueur2 = nickname
                    else:
                        Joueur1 = nickname
                    clients[nickname] = sc #gives a name to the socket
                    print("client connected : ", nickname)
                    nicknames.append(nickname)
                    for other, socket_value in clients.items():
                        if other != nickname and socket_value != "serveur": #don't send message to self nor to server #SEND message to everyone about the new client who connected 
                            print("aaaaaaaaaaaaaaa : " + str(socket_value) + " BBBBB " + str(type(socket_value)))
                            socket_value.send("client connected : ".encode() + nickname.encode() + " \n".encode())
                        else:
                            None
                        try:
                             msg = x.recv(1500)
                        except:
                            None
                        gamemode = "multiplayer"
                        grids = [grid(), grid(), grid()]
                        current_player = J1
                        #grids[J1].display()
                        while grids[0].gameOver() == -1:
                            if gamemode == "multiplayer":
                                while (len(nicknames) == 1):
                                    print("aie ! on se sent seul ici !")
                                    time.sleep(5)
                                while (len(nicknames) == 2):
                                    print("il y a : une personne en attente")
                                    time.sleep(5)
                                while (len(nicknames) > 2):
                                    clients[nicknames[current_player]].sendall("Waiting For player".encode())
                                    time.sleep(1)
                                    clients[nicknames[current_player]].sendall("Waiting For player•".encode())
                                    time.sleep(1)
                                    clients[nicknames[current_player]].sendall("Waiting For player••".encode())
                                    time.sleep(1)
                                    clients[nicknames[current_player]].sendall("Waiting For player•••".encode())
                                    time.sleep(1)
                                    print(nicknames)
                                    print(len(nicknames))
                                shot = -1
                                while shot <0 or shot >=NB_CELLS:
                                    clients[nicknames[current_player]].sendall(str(grids[current_player]).encode())
                                    clients[nicknames[current_player]].sendall("quelle case allez-vous jouer ?".encode())
                                    data = "no"
                                    while (data == "no"):
                                        print (data)
                                        time.sleep(0.5)
                                        data = clients[nicknames[current_player]].recv(1500).decode()
                                        try:
                                            data = int(data)
                                        except:
                                            clients[nicknames[current_player]].sendall("Vous devez écrire un chiffre entre 0 et 8".encode())
                                            break
                                        shot = data
                                        data = "no"
                                    if (grids[0].cells[shot] != EMPTY):
                                        grids[current_player].cells[shot] = grids[0].cells[shot]
                                        grids[0].display()
                                    else:
                                        grids[current_player].cells[shot] = current_player
                                        grids[0].play(current_player, shot)
                                        current_player = "current_player%2+1"
                                        grids[0].display()
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
