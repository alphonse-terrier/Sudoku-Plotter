#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import numpy as np
import threading as th

import save
import lcd3


class Server(th.Thread):
    """
    Genere la creation d'une connexion sur le reseau local (serveur)
    afin de communiquer par exemple avec un PC distant (client)
    """

    def __init__(self, boss):
        th.Thread.__init__(self)
        self.boss = boss
        self.power = True
        self.host = ""
        self.port = 50000
        self.sudoku = np.zeros((9, 9), int)
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tryConnect(self):
        try:
            self.mySocket.bind((self.host, self.port))
        except socket.error:
            lcd3.write("Connection failed")
            sys.exit()

    def run(self):
        self.tryConnect()
        self.starting()

    def starting(self):
        self.mySocket.listen(5)
        connexion, adresse = self.mySocket.accept()
        lcd3.write("connected to  ip " + str(adresse[0]))
        while self.power:
            try:
                text = connexion.recv(1024).decode()
                if not text:
                    self.starting()
                elif text == "reboot":
                    connexion.send("raspi_reboot".encode())
                    lcd3.write("Sudoku Plotter rebooting...")
                    os.system("reboot")
                elif text == "shutdown":
                    connexion.send("raspi_shutdown".encode())
                    lcd3.write("Sudoku Plotter Goodbye!")
                    self.boss.stop()
                    os.system("sudo shutdown -h now")
                elif text == "photo":
                    connexion.send("photo_taken".encode())
                    lcd3.write("one photo has been taken")
                elif text == "stop":
                    lcd3.write("Sudoku writing process stopped!")
                    self.boss.sleep()
                else:
                    try:
                        self.sudoku = save.stringToSudoku(text)
                        connexion.send("sudoku_received".encode())
                        self.boss.writeSudoku(self.sudoku)
                    except IndexError or ValueError:
                        self.sudoku = np.zeros((9, 9), int)
            except ConnectionAbortedError or ConnectionResetError:
                lcd3.write("Client disconnected")
                self.starting()
            time.sleep(0.1)

    def stop(self):
        self.mySocket.close()


if __name__ == "__main__":
    class Boss:
        def __init__(self):
            self.sudoku = np.zeros((9, 9), int)

        def writeSudoku(self, sudoku):
            self.sudoku = sudoku
            print(self.sudoku, '\n')

    Server(Boss).start()
