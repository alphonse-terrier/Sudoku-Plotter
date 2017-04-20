#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np

import lcd3
import write
import server
import step_motor as stp


class Main:
    def __init__(self):
        self.power = True
        self.sudoku = np.zeros((9, 9), int)
        self.Write = write.Write()
        self.Server = server.Server(self)
        self.MotorControl = stp.MotorControl()
        lcd3.write("Sudoku Plotter Welcome!")

    def start(self):
        self.Server.start()
        time.sleep(1)
        while self.power:
            time.sleep(1)

    def writeSudoku(self, sudoku):
        self.sudoku = sudoku
        print(sudoku)
        lcd3.write("Sudoku writing in progress...")
        points = self.Write.writeSudoku(sudoku)
        while self.MotorControl.getPoints():
            time.sleep(1)
        self.MotorControl.setPoins(points)
        self.MotorControl.movingMotor()

    def stop(self):
        self.power = False
        self.Server.stop()
        self.MotorControl.stop()


if __name__ == "__main__":
    Main().start()
