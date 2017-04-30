#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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
        os.chdir("/home/pi/Desktop/Sudoku-Plotter/script")
        lcd3.write("Sudoku Plotter Welcome!")

    def start(self):
        self.Server.start()
        """time.sleep(1)
        self.Write.writeLine(3, 5, 3, 20)
        self.Write.writeLine(3, 20, 18, 20)
        self.Write.writeLine(18, 20, 18, 5)
        self.Write.writeLine(18, 5, 3, 5)
        points = self.Write.points
        points.insert(0, "down")
        points.append("up")
        print(points)
        self.MotorControl.setPoins(points)
        self.MotorControl.movingMotor()"""
        while self.power:
            time.sleep(1)
  
    def writeSudoku(self, sudoku):
        try:
            self.sudoku = sudoku
            print(sudoku)
            lcd3.write("Sudoku writing in progress...")
            points = self.Write.writeSudoku(sudoku)
            while self.MotorControl.getPoints():
                time.sleep(1)
            self.MotorControl.setPoins(points)
            self.MotorControl.movingMotor()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.power = False
        self.Server.stop()
        self.MotorControl.stop()


if __name__ == "__main__":
    Main().start()
