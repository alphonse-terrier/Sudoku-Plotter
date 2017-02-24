#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import threading

import lcd
import save
import numpy as np
import button as bt
import camera as cm
import resolution as rs


class Sudoku:
    def __init__(self):
        self.number = 0
        self.errors = []
        self.taille = (3, 3)
        self.power = True
        self.power_mode = True
        self.select_mode = None
        self.modes = ["Automatic", "Practice"]
        self.mode = self.modes[self.number]
        self.nb_cases = self.taille[0] * self.taille[1]
        self.sudoku = np.zeros((self.nb_cases, self.nb_cases), int)
        self.liste_position = []
        self.methode_resolution = "Backtracking"

        self.stop = Stop(self)
        self.camera = cm.Camera(self)
        self.resolution = rs.Resolution(self)
        self.button = bt.Buttons([11, 13, 15])

    def start(self):
        while self.power:
            lcd.write("Sudoku Plotter Welcome!")
            bt_pressed = self.wait(5)
            if bt_pressed[2]:
                self.quit()
            elif bt_pressed[1]:
                self.button.pressed = [0, 0, 0]
                lcd.write("Choose the mode")
                lcd.write(self.mode + "?", 2)
                time.sleep(4)
                while self.power_mode:
                    if self.button.pressed[0]:
                        self.button.pressed[0] = 0
                        self.number = 1 - self.number
                        self.mode = self.modes[self.number]
                        lcd.write(self.mode + "?", 2)
                        time.sleep(2)

                    if self.button.pressed[1]:
                        self.button.pressed[1] = 0
                        self.select_mode = self.mode

                    if self.button.pressed[2]:
                        self.button.pressed[2] = 0
                        self.quit()

                    if self.select_mode == "Automatic":
                        lcd.write("Sudoku Plotter Automatic Mode")
                        time.sleep(2)
                        self.stop.run()
                        self.automaticMode()

                    if self.select_mode == "Practice":
                        lcd.write("Sudoku Plotter Practice Mode")
                        time.sleep(2)
                        self.practiceMode()

                    if self.select_mode:
                        self.select_mode = None
                        self.start()

                    time.sleep(1)
            time.sleep(1)

        lcd.write("Sudoku Plotter Goodbye!")
        time.sleep(2)
        self.power = False
        self.stop.power = False
        self.button.stop()
        os.system("sudo shutdown -h now")

    def automaticMode(self):
        lcd.write("Photo Capture... Please Wait!")
        self.camera.takePhoto()
        if "camera_error" not in self.errors:
            lcd.write("Succeeded!", 2)
            time.sleep(2)
        else:
            lcd.write("Camera isn't connected!")
            time.sleep(3)
            lcd.write("Camera error Continue?")
            time.sleep(4)
            if self.button.pressed[2]: self.start()
        lcd.write("Recognition...")
        lcd.write("Please Wait!", 2)
        os.system("sudo python extraction.py")
        lcd.write("Succeeded!", 2)
        time.sleep(2)
        lcd.write("Solving... Please Wait!")
        time.sleep(0.5)
        self.sudoku = save.readSudoku()
        self.sudoku, self.liste_position = self.resolution.start(self.sudoku, self.methode_resolution)
        if "sudoku_insoluble" not in self.errors:
            lcd.write("Succeeded!", 2)
            print("finished /n", self.sudoku)
            time.sleep(2)
            lcd.write("Sudoku Plotter completed!", 2)

        if self.errors and self.errors != ["camera_error"]:
            lcd.write("Failed!", 2)
            self.wait()
            self.errors = []
            self.start()

    def practiceMode(self):
        pass

    def wait(self, sleep=2):
        previous_time = time.time()
        while time.time() - previous_time < sleep:
            if self.button.pressed is not None:
                bt = self.button.pressed
                self.button.pressed = [0, 0, 0]
                return bt
            time.sleep(0.1)
        return [0, 0, 0]

    def setError(self, error):
        if error not in self.errors:
            self.errors.append(error)

    def quit(self):
        lcd.write("Sudoku Plotter Goodbye?")
        time.sleep(2)
        bt_pressed = self.wait(4)
        if bt_pressed[1] or bt_pressed[2]:
            self.power = False
            self.power_mode = False
            self.start()


class Stop(threading.Thread):
    def __init__(self, boss):
        threading.Thread.__init__(self)
        self.power = True
        self.boss = boss

    def start(self):
        while self.power:
            if self.boss.button[2]:
                self.boss.power = False
                self.boss.power_mode = False
                self.boss.start()
                self.power = False

"""
    def start(self):
        lcd.write("Sudoku Plotter Welcome!")
        time.sleep(2)
        while self.power:
            lcd.write("Sudoku Plotter Welcome!")
            print("Welcome")
            if self.button.pressed == 0:
                self.button.pressed = None
                self.number = 1 - self.number
                self.mode = self.modes[self.number]

            if self.button.pressed == 1:
                self.button.pressed = None
                self.select_mode = self.mode

            if self.button.pressed == 2:
                self.button.pressed = None
                lcd.write("Goodbye?", 2)
                while not self.button.pressed:
                    time.sleep(0.1)
                if self.button.pressed == 1:
                    self.power = False
                self.button.pressed = None

            while self.select_mode == "automatic":
                lcd.write("Automatic?", 2)
                if self.button.pressed == 2:
                    self.select_mode = None
                    self.button.pressed = None

            while self.select_mode == "practice":
                lcd.write("Practice?", 2)
                if self.button.pressed == 2:
                    self.select_mode = None
                    self.button.pressed = None

            time.sleep(2)
        print("Bye!")
"""

lcd = lcd.LCD()
sudoku = Sudoku()
sudoku.button.start()
sudoku.start()

"""
import resolution as rs
import camera as cm
import step_motor as stp
import os

lcd = lcd.LCD()
lcd.write("Sudoku Plotter Welcome!")
time.sleep(2)
lcd.write("Automatic?", 2)
time.sleep(2)
lcd.write("Practice?", 2)
time.sleep(2)
lcd.write("Step by step?", 2)
time.sleep(2)
lcd.write("Photo capture in progress...")
time.sleep(2)
lcd.write("Use the joystick to move or write")
time.sleep(2)
lcd.write("Joystick isn't connected!")
time.sleep(2)
lcd.write("Recognition...")
lcd.write("in progress...", 2)
time.sleep(2)
lcd.write("Failed!", 2)
time.sleep(2)
lcd.write("Succeeded!", 2)
time.sleep(2)
lcd.write("Solving...")
time.sleep(2)
lcd.write("Sudoku Plotter Goodbye!")
"""
