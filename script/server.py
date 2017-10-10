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
    Genere la creation b'une connexion sur le reseau local (serveur)
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
                    lcd3.write("Sudoku Plotter rebooting...")
                    connexion.send("raspi_reboot".encode())
                    os.system("reboot")
                elif text == "shutdown":
                    lcd3.write("Sudoku Plotter Goodbye!")
                    connexion.send("raspi_shutdown".encode())
                    self.boss.stop()
                    os.system("sudo shutdown -h now")
                elif text == "photo":
                    lcd3.write("a photo was taken")
                    self.boss.takePhoto()
                    sudoku = save.readSudoku("/home/pi/Desktop/Sudoku-Plotter/sudoku/Sudoku.txt")
                    sudoku_string = save.sudokuToString(sudoku)
                    connexion.send(sudoku_string.encode())
                elif text == "stop":
                    lcd3.write("Sudoku writing process stopped!")
                    connexion.send("raspi_stop".encode())
                    self.boss.sleep()
                elif text == "up" or text == "down":
                    connexion.send(text.encode())
                    self.boss.setPenPosition(text)
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
