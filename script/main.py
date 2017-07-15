#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import tkinter as tk

import client
import write as w
import display as dp
import resolution as rs


class Main:
    """
    Permet la gestion des sudoku à savoir :
        - leur édition par l'utilisateur pour obtenir le sudoku à résoudre
        - leur résolution à l'aide de différentes méthodes de résolution:
            - inclusion
            - exclusion
            - backtracking
            - ...
        - leur affichage à l'aide du module tkinter
    """

    def __init__(self):
        self.beta_version = True
        self.error = []
        self.taille = (3, 3)
        self.mode = "Directe"
        self.nb_cases = self.taille[0] * self.taille[1]
        self.sudoku = np.zeros((self.nb_cases, self.nb_cases), int)
        self.methode_resolution = "Globale"
        self.liste_position = []

        self.W = w.Write()
        self.Client = client.Client(self)
        self.Resolution = rs.Resolution(self)
        self.Display = dp.Display(self)
        self.Resolution.start()

        self.Display.mainloop()

    def setError(self, error, leave=True):
        if leave:
            if error not in self.error:
                self.error.append(error)
            try: self.Display.showError(error)
            except AttributeError: pass
        else:
            if error in self.error:
                self.error.remove(error)

    def showInfo(self, info):
        self.Display.showInfo(info)

    def getError(self):
        return self.error

    def setMethodeResolution(self, methode):
        self.methode_resolution = methode

    def startResolution(self, sudoku):
        self.Resolution.update(sudoku, self.methode_resolution)
        if self.mode == "Directe":
            self.Resolution.sleep = 0
            self.sudoku, self.liste_position = self.Resolution.begin()
            self.Display.updateSudoku(self.sudoku, self.liste_position)
        else:
            self.Resolution.process = True
            while self.Resolution.process:
                time.sleep(self.Resolution.sleep)
                try:
                    self.Display.updateSudoku(self.Resolution.sudoku, self.Resolution.starting_possibilities)
                except tk.TclError:
                    pass

    def startAll(self):
        self.Client.sendInfo("photo")
        if self.Display.showInfo("continuer"):
            self.sudoku = self.Display.sudoku
            self.startResolution(self.sudoku)

    def pauseResolution(self):
        self.Resolution.wait()

    def stopResolution(self):
        self.Resolution.resolution = self.Resolution.process = self.Resolution.back_tracking = False

    def setSudoku(self, sudoku):
        self.sudoku = sudoku

    def sendSudoku(self, evt=None):
        self.sudoku = self.Display.sudoku
        self.Client.sendSudoku(self.sudoku)

    def sendInfo(self, info):
        self.Client.sendInfo(info)

    def setMode(self, mode):
        self.mode = mode
        if mode == "Rapide": self.Resolution.sleep = 0.01
        if mode == "Lente": self.Resolution.sleep = 0.1

    def closeAll(self):
        self.stopResolution()
        self.Resolution.power = False
        self.Display.destroy()
        self.Client.close()


Main()
