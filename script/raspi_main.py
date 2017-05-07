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
    """
    Classe principale pour la Raspberry Pi
    S'occupe de la gestion des différents scripts afin 
    de les faire communiquer les uns avec les autres 
    """

    def __init__(self):

        self.power = True
        self.sudoku = np.zeros((9, 9), int)
        self.Write = write.Write()
        self.Server = server.Server(self)
        self.MotorControl = stp.MotorControl()
        self.MotorControl.start()
        os.chdir("/home/pi/Desktop/Sudoku-Plotter/script/lcd")
        lcd3.write("Sudoku Plotter Welcome!")

    def start(self):
        self.Server.start()
        while self.power:
            time.sleep(1)

    def writeSudoku(self, sudoku):
        try:
            self.sudoku = sudoku
            print(sudoku)
            points = self.Write.writeSudoku(sudoku)
            while self.MotorControl.getPoints():
                time.sleep(1)
            lcd3.write("Initialisation of the position")
            self.MotorControl.initializePosition()
            lcd3.write("Sudoku writing in progress...")
            self.MotorControl.points = points
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.power = False
        self.Server.stop()
        self.MotorControl.stop()

    def sleep(self):
        self.MotorControl.points = ["up"]
        self.MotorControl.sleep()


if __name__ == "__main__":
    Main().start()
