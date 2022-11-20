#!/usr/bin/python3

from platform import java_ver
from grid import *
import  random
from pickle import NONE
import socket
import select
import time
import pdb

def main():
    serv = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(("", 7777))
    serv.listen(1)
    clients = {serv:"serveur"}
    sockets,l1,l2 = [serv],[],[]
    nicknames = ["serv"]
    #pdb.set_trace()

    while True:
            reader, writer, error = select.select(sockets,l1,l2)
            for x in reader:
                if x == serv:
                    sc, a = serv.accept()
                    nickname = str(sc.getpeername()) #gives out nickname
                    clients[nickname] = sc #gives a name to the socket
                    print("client connected : ", nickname)
                    nicknames.append(nickname)
                    for other, socket_value in clients.items():
                        if other != nickname and socket_value != "serveur": #don't send message to self nor to server #SEND message to everyone about the new client who connected 
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
                        clients[nicknames[current_player]].sendall("Quel mode de jeu souhaitez vous jouez ? \n 1 pour solo \n n'importe quel autre charactère lancera la recherche multijoueur \n".encode())
                        data = clients[nicknames[current_player]].recv(1500).decode()
                        try:
                            data = int(data)
                        except:
                            clients[nicknames[current_player]].sendall("Vous devez choisir entre 1 et 2".encode())
                            break  
                        if (data == 1):
                            gamemode = "solo"
                        #grids[J1].display()
                        while grids[0].gameOver() == -1:
                            if gamemode == "multiplayer":
                                while (len(nicknames) == 1):
                                    print("aie ! on se sent seul ici !")
                                    time.sleep(5)
                                while (len(nicknames) == 2):
                                    print("il y a : une personne en attente")
                                    clients[nicknames[current_player]].sendall("Waiting For player".encode())
                                    time.sleep(1)
                                    clients[nicknames[current_player]].sendall("Waiting For player•".encode())
                                    time.sleep(1)
                                    clients[nicknames[current_player]].sendall("Waiting For player••".encode())
                                    time.sleep(1)
                                    clients[nicknames[current_player]].sendall("Waiting For player•••".encode())
                                    time.sleep(1)

                                    sc, a = serv.accept()
                                    nickname = str(sc.getpeername()) #gives out nickname
                                    clients[nickname] = sc #gives a name to the socket
                                    print("client connected : ", nickname)
                                    nicknames.append(nickname)
                                    sc.sendall("you are connected, it's your opponent's turn \n ".encode())
                                    for other, socket_value in clients.items():
                                        if other != nickname and socket_value != "serveur": #don't send message to self nor to server #SEND message to everyone about the new client who connected 
                                            socket_value.send("client connected : ".encode() + nickname.encode() + " \n".encode())
                                        else:
                                            None
                                shot = -1
                                while shot <0 or shot >=NB_CELLS:
                                    clients[nicknames[current_player]].sendall(str(grids[current_player]).encode() +  " \n ".encode())
                                    time.sleep(0.05) #Without that, the third time in this loop sends both upper and lower line at the exact same time, making it look like only one sendall.
                                    clients[nicknames[current_player]].sendall("quelle case allez-vous jouer ?".encode() +  " \n ".encode())
                                    data = "no"
                                    while (data == "no"):
                                        time.sleep(0.5)
                                        data = clients[nicknames[current_player]].recv(1500).decode()
                                        try:
                                            data = int(data)
                                        except:
                                            clients[nicknames[current_player]].sendall("Vous devez écrire un chiffre entre 0 et 8, trompez vous, et se sera votre défaite".encode() +  " \n ".encode())
                                            time.sleep(0.05) #Without that, the third time in this loop sends both upper and lower line at the exact same time, making it look like only one sendall.
                                            clients[nicknames[current_player]].sendall("quelle case allez-vous jouer ? \n".encode())
                                            data = clients[nicknames[current_player]].recv(1500).decode()
                                            try:
                                                data = int(data)
                                            except:
                                                clients[nicknames[current_player]].sendall("Dommage, vous perdez par forfait ! \n".encode())
                                                clients[nicknames[current_player]].sendall("END".encode())
                                                current_player = current_player%2+1
                                                clients[nicknames[current_player]].sendall("Votre adversaire a abandonner ! \n".encode())
                                                clients[nicknames[current_player]].sendall("END".encode())
                                                break
                                        shot = data
                                    if (grids[0].cells[shot] != EMPTY):
                                        grids[current_player].cells[shot] = grids[0].cells[shot]
                                        grids[0].display()
                                    else:
                                        grids[current_player].cells[shot] = current_player
                                        grids[0].play(current_player, shot)
                                        current_player = current_player%2+1
                                        grids[0].display()

                            else: #Jeu solo
                                print("SOLO GAME")
                                if current_player == J1:
                                    shot = -1
                                    while shot <0 or shot >=NB_CELLS:
                                        clients[nicknames[current_player]].sendall(str(grids[current_player]).encode() +  " \n ".encode())
                                        time.sleep(0.05) #Without that, the third time in this loop sends both upper and lower line at the exact same time, making it look like only one sendall.
                                        clients[nicknames[current_player]].sendall("quelle case allez-vous jouer ? \n".encode())

                                        data = clients[nicknames[current_player]].recv(1500).decode()
                                        
                                        try:
                                            data = int(data)
                                        except:
                                            clients[nicknames[current_player]].sendall("Vous devez écrire un chiffre entre 0 et 8, trompez vous, et se sera votre défaite \n".encode())
                                            time.sleep(0.05) #Without that, the third time in this loop sends both upper and lower line at the exact same time, making it look like only one sendall.
                                            clients[nicknames[current_player]].sendall("quelle case allez-vous jouer ? \n".encode())
                                            data = clients[nicknames[current_player]].recv(1500).decode()
                                            try:
                                                data = int(data)
                                            except:
                                                clients[nicknames[current_player]].sendall("Dommage, vous perdez par forfait ! \n".encode())
                                                clients[nicknames[current_player]].sendall("END".encode())
                                                break

                                               
                                        shot = data
                                else:
                                    shot = random.randint(0,8)
                                    while grids[current_player].cells[shot] != EMPTY:
                                        shot = random.randint(0,8)
                                if (grids[0].cells[shot] != EMPTY):
                                    grids[current_player].cells[shot] = grids[0].cells[shot]
                                else:
                                    grids[current_player].cells[shot] = current_player
                                    grids[0].play(current_player, shot)
                                    current_player = current_player%2+1
                                if current_player == J1:
                                    grids[0].display() #grid[J1]
                        print("Partie terminée")
                        grids[0].display()
                        if grids[0].gameOver() == J1:
                            if (gamemode == "solo"):
                                clients[nicknames[J1]].sendall("Vous avez gagné !".encode())
                                time.sleep(0.05) #Without that, it sends both upper and lower line at the exact same time, making it look like only one sendall.
                                time.sleep(0.05) #Without that, it sends both upper and lower line at the exact same time, making it look like only one sendall.
                                clients[nicknames[J1]].sendall(str(grids[0]).encode())
                                time.sleep(0.05) #Without that, it sends both upper and lower line at the exact same time, making it look like only one sendall.
                                clients[nicknames[J1]].sendall("END".encode())
                                break
                            else:    
                                clients[nicknames[J1]].sendall("Vous avez gagné !".encode())
                                clients[nicknames[J2]].sendall("Vous avez perdu !".encode())
                                clients[nicknames[J2]].sendall(str(grids[0]).encode())
                                clients[nicknames[J1]].sendall(str(grids[0]).encode())
                                time.sleep(0.1)
                                clients[nicknames[J2]].sendall("END".encode())
                                clients[nicknames[J1]].sendall("END".encode())
                                break
                        elif(grids[0].gameOver() == J2):
                            if (gamemode == "solo"):
                                clients[nicknames[J1]].sendall("Vous avez perdu !".encode())
                                clients[nicknames[J1]].sendall(str(grids[0]).encode())
                                time.sleep(0.05) #Without that, it sends both upper and lower line at the exact same time, making it look like only one sendall.
                                clients[nicknames[J1]].sendall("END".encode())
                                break
                            else:
                                clients[nicknames[J1]].sendall("Vous avez perdu !".encode())
                                clients[nicknames[J2]].sendall("Vous avez gagné !".encode())
                                clients[nicknames[J2]].sendall(str(grids[0]).encode())
                                clients[nicknames[J2]].sendall(str(grids[0]).encode())
                                time.sleep(0.1)
                                clients[nicknames[J2]].sendall("END".encode())
                                clients[nicknames[J1]].sendall("END".encode())
                                break
                        else:
                            if (gamemode == "solo"):
                                clients[nicknames[J1]].sendall("Egalité !".encode())
                                clients[nicknames[J1]].sendall(str(grids[0]).encode())
                                time.sleep(0.05) #Without that, it sends both upper and lower line at the exact same time, making it look like only one sendall.
                                clients[nicknames[J1]].sendall("END".encode())
                                break
                            else:
                                clients[nicknames[J1]].sendall("Egalité !".encode())
                                clients[nicknames[J2]].sendall("Egalité !".encode())
                                clients[nicknames[J2]].sendall(str(grids[0]).encode())
                                clients[nicknames[J2]].sendall(str(grids[0]).encode())
                                time.sleep(0.1)
                                clients[nicknames[J2]].sendall("END".encode())
                                clients[nicknames[J1]].sendall("END".encode())
                                break

                        
main()