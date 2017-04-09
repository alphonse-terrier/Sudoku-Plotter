#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np

import lcd3
import write
import server
# import button as bt
import step_motor as stp


class Main:
    def __init__(self):
        self.power = True
        self.sudoku = np.zeros((9, 9), int)
        self.W = write.Write()
        # self.button = bt.Button([11, 13, 15])
        lcd3.write("Sudoku Plotter Welcome!")
        self.Server = server.Server(self)

    def start(self):
        self.Server.start()
        time.sleep(1)
        while self.power:
            time.sleep(1)

    def writeSudoku(self, sudoku):
        self.sudoku = sudoku
        print(sudoku)
        lcd3.write("Sudoku writing in progress...")

    def stop(self):
        self.Server.stop()
        self.power = False


if __name__ == "__main__":
    Main().start()
