#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import socket
import numpy as np
import threading as th

import save
import lcd3


class Server(th.Thread):
    def __init__(self, boss):
        th.Thread.__init__(self)
        self.boss = boss
        self.power = True
        self.host = ""
        self.port = 50000
        self.sudoku = np.zeros((9, 9), int)
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tryConnect()

    def tryConnect(self):
        try:
            self.mySocket.bind((self.host, self.port))
        except socket.error:
            lcd3.write("Connection failed")
            sys.exit()

    def run(self):
        self.starting()

    def starting(self):
        self.mySocket.listen(5)
        connexion, adresse = self.mySocket.accept()
        lcd3.write("connected to  ip " + str(adresse[0]))
        while self.power:
            try:
                sudoku_string = connexion.recv(1024).decode()
                self.sudoku = save.stringToSudoku(sudoku_string)
                connexion.send("sudoku_received".encode())
                self.boss.writeSudoku(self.sudoku)
            except IndexError:
                time.sleep(0.1)
                self.starting()
            except ConnectionAbortedError:
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
