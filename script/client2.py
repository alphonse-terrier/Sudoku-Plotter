#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import socket
import numpy as np
import threading as th

import save


class Client:
    def __init__(self, boss):
        self.boss = boss
        self.host = "localhost"  # "192.168.43.101"
        self.port = 50000
        self.seen = False
        self.power = True
        self.connected = False
        self.sudoku = np.zeros((9, 9), int)
        self.sudoku_string = save.sudokuToString(save.readSudoku())
        self.mySocket = None
        self.Receive = self.Receive(self)
        self.tryConnect()
        self.Receive.start()

    def tryConnect(self):
        if not self.connected:
            try:
                self.mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.mySocket.connect((self.host, self.port))
                self.connected = True
                print("Server connected")
            except socket.error:
                self.connected = False
                self.boss.setError("raspi_connection")
                time.sleep(2)
                self.tryConnect()

    def read(self):
        zero_time = time.time()
        while 0 < 10:
            if not self.seen and self.Receive.text:
                text = self.Receive.text
                self.Receive.text = []
                self.seen = True
                return text
        return 0

    def sendSudoku(self, sudoku):
        if self.connected:
            try:
                self.sudoku = sudoku
                self.sudoku_string = save.sudokuToString(self.sudoku)
                self.mySocket.send(self.sudoku_string.encode())
                msgServer = self.read()
                if msgServer: self.boss.showInfo(msgServer)
                else: self.boss.setError("raspi_connection")
            except ConnectionResetError:
                self.boss.setError("raspi_connection")
                self.connected = False
                self.tryConnect()

    def rebootRaspi(self):
        if self.connected:
            try:
                self.mySocket.send("reboot".encode())
                msgServer = self.read()
                if msgServer: self.boss.showInfo(msgServer)
            except ConnectionResetError:
                self.boss.setError("raspi_connection")
                self.connected = False
                self.tryConnect()

    def shutdownRaspi(self):
        if self.connected:
            try:
                self.mySocket.send("shutdown".encode())
                msgServer = self.read()
                if msgServer: self.boss.showInfo(msgServer)
            except ConnectionResetError:
                self.boss.setError("raspi_connection")
                self.connected = False
                self.tryConnect()


    def stop(self):
        self.power = False
        self.connected = False
        self.mySocket.close()


    class Receive(th.Thread):
        def __init__(self, boss):
            th.Thread.__init__(self)
            self.boss = boss
            self.text = []

        def run(self):
            while self.boss.power:
                if self.boss.connected:
                    try:
                        self.text.append(self.boss.mySocket.recv(1024).decode())
                        self.boss.seen = False
                    except ConnectionResetError:
                        self.boss.connected = False
                        self.boss.boss.setError("raspi_connection")
                else:
                    self.boss.tryConnect()
                time.sleep(0.1)


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
