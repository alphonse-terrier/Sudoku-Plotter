#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import numpy as np

import save
import write as w
import camera as cm
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
        self.nb_cases = self.taille[0] * self.taille[1]
        self.sudoku = np.zeros((self.nb_cases, self.nb_cases), int)
        self.methode_resolution = "Globale"
        self.liste_position = []

        self.W = w.Write()
        self.Camera = cm.Camera(self)
        self.Display = dp.Display(self)
        self.Resolution = rs.Resolution(self)

        self.Display.mainloop()


    def setError(self, error, off=True):
        if off:
            if error not in self.error:
                self.error.append(error)
        else:
            if error in self.error:
                self.error.remove(error)

    def getError(self):
        return self.error

    def setMethodeResolution(self, methode):
        self.methode_resolution = methode

    def startResolution(self, sudoku):
        self.sudoku, self.liste_position = self.Resolution.start(sudoku, self.methode_resolution)
        self.Display.updateSudoku(self.sudoku, self.liste_position)

    def stopResolution(self):
        pass

    def setSudoku(self, sudoku):
        self.sudoku = sudoku

    def writeSudoku(self, sudoku):
        self.sudoku = sudoku
        save.saveSudoku(sudoku)
        os.system("sudo python3 writing_main.py")


Main()
