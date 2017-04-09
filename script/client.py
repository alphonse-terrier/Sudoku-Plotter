#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import numpy as np

import save


class Client:
    def __init__(self, boss):
        self.boss = boss
        self.host = "192.168.43.101"
        self.port = 50000
        self.power = True
        self.connected = False
        self.sudoku = np.zeros((9, 9), int)
        self.sudoku_string = save.sudokuToString(save.readSudoku())

        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tryConnect()

    def tryConnect(self):
        if not self.connected:
            try:
                self.mySocket.connect((self.host, self.port))
                self.connected = True
                print("Server connected")
            except socket.error:
                self.connected = False
                self.boss.setError("raspi_connection")

    def sendSudoku(self, sudoku):
        if self.connected:
            try:
                self.sudoku = sudoku
                self.sudoku_string = save.sudokuToString(self.sudoku)
                self.mySocket.send(self.sudoku_string.encode())
                msgServer = self.mySocket.recv(1024)
                self.boss.showInfo(msgServer.decode())
            except ConnectionResetError:
                self.boss.setError("raspi_connection")

    def stop(self):
        self.power = False
        self.mySocket.close()


if __name__ == "__main__":
    class Boss:
        def __init__(self):
            self.sudoku = np.zeros((9, 9), int)

        def showInfo(self, info):
            print(info)

    Boss = Boss()
    c = Client(Boss)
    c.sendSudoku(Boss.sudoku)
