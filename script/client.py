#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import socket
import numpy as np

import save


class Client:
    def __init__(self, boss):
        self.boss = boss
        self.host = "localhost"  # "192.168.43.101"
        self.port = 50000
        self.power = True
        self.connected = False
        self.sudoku = np.zeros((9, 9), int)
        self.sudoku_string = ""
        self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tryConnect(self):
        if not self.connected:
            try:
                self.mySocket.connect((self.host, self.port))
                self.connected = True
                print("Server connected")
            except socket.error:
                self.connected = False
                self.boss.setError("raspi_connection")
        return self.connected

    def sendSudoku(self, sudoku):
        if self.tryConnect():
            try:
                self.sudoku = sudoku
                self.sudoku_string = save.sudokuToString(self.sudoku)
                self.mySocket.send(self.sudoku_string.encode())
                msgServer = self.mySocket.recv(1024).decode()
                self.boss.showInfo(msgServer)
            except ConnectionResetError:
                self.boss.setError("raspi_connection")

    def sendInfo(self, info):
        if self.tryConnect():
            try:
                self.mySocket.send(info.encode())
                msgServer = self.mySocket.recv(1024).decode()
                if msgServer: self.boss.showInfo(msgServer)
            except ConnectionResetError:
                self.boss.setError("raspi_connection")
                self.connected = False

    def stop(self):
        self.power = False
        self.mySocket.close()


if __name__ == "__main__":
    class Boss:
        def __init__(self):
            self.sudoku = np.zeros((9, 9), int)

        def showInfo(self, info):
            print(info)

        def setError(self, error):
            print(error)

    Boss = Boss()
    c = Client(Boss)
    c.sendSudoku(Boss.sudoku)
    c.sendInfo("shutdown")
