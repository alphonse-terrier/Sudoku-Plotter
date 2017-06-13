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
            lcd3.write("Initialisation of the position")
            self.MotorControl.initializePosition()
            lcd3.write("Sudoku writing in progress...")
            self.MotorControl.points = []
            self.MotorControl.setPoints(self.Write.writeSudoku(sudoku))
            lcd3.write("Sudoku Plotter Welcome!")
        except KeyboardInterrupt:
            self.stop()

    def setPenPosition(self, text):
        lcd3.write("Sudokku Plotter position set")
        if not self.MotorControl.getPoints():
            self.MotorControl.points = [text]

    def takePhoto(self):
        os.chdir("/home/pi/Desktop/Sudoku-Plotter/script")
        os.system("raspistill -o ../pictures/Sudoku.jpg")
        os.system("sudo python extraction.py")

    def stop(self):
        self.power = False
        self.Server.stop()
        self.MotorControl.points = ["up"]
        self.MotorControl.stop()

    def sleep(self):
        self.MotorControl.points = ["up"]
        self.MotorControl.sleep()


if __name__ == "__main__":
    Main().start()
