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
        self.host = ""
        self.port = 50000
        self.seen = False
        self.power = True
        self.connexion = None
        self.connected = False
        self.sudoku = np.zeros((9, 9), int)
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Receive = self.Receive(self)
        self.tryConnect()
        self.Receive.start()

    def tryConnect(self):
        try:
            self.mySocket.bind((self.host, self.port))
            self.connected = True
        except socket.error:
            self.connected = False
            lcd3.write("Connection failed!")
            time.sleep(2)
            self.tryConnect()

    def run(self):
        self.starting()

    def read(self):
        zero_time = time.time()
        while 0 < 10:
            if not self.seen and self.Receive.text:
                text = self.Receive.text
                self.Receive.text = []
                self.seen = True
                return text
        return 0

    def starting(self):
        lcd3.write("Server connected waiting...")
        self.mySocket.listen(5)
        self.connexion, adresse = self.mySocket.accept()
        lcd3.write("connected to " + str(adresse[0]) + " ip")
        while self.power:
            try:
                sudoku_string = self.read()[0]
                if sudoku_string: self.sudoku = save.stringToSudoku(sudoku_string)
                self.connexion.send("sudoku_received".encode())
                # self.boss.writeSudoku(self.sudoku)
                print(self.sudoku)
            except IndexError:
                time.sleep(0.1)
                self.starting()
            except ConnectionAbortedError or ConnectionResetError:
                lcd3.write("Client disconnected")
                self.starting()

            time.sleep(0.1)

    def stop(self):
        self.power = False
        self.mySocket.close()


    class Receive(th.Thread):
        def __init__(self, boss):
            th.Thread.__init__(self)
            self.boss = boss
            self.text = []

        def run(self):
            while self.boss.power:
                try:
                    if self.boss.connected and self.boss.connexion:
                        self.text.append(self.boss.connexion.recv(1024).decode())
                        self.boss.seen = False
                except ConnectionAbortedError or ConnectionResetError:
                    lcd3.write("Client disconnected")
                time.sleep(0.1)


if __name__ == "__main__":
    class Boss:
        def __init__(self):
            self.sudoku = np.zeros((9, 9), int)

        def writeSudoku(self, sudoku):
            self.sudoku = sudoku
            print(self.sudoku, '\n')


    Server(Boss).start()