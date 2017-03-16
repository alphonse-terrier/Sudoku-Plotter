# -*- coding: utf-8 -*-
# !usr/bin/env python

import numpy as np


def saveSudoku(sudoku):
    """
    Enregistre la grille dans un fichier texte
    :param sudoku:
    :return: None
    """
    fichier = open("../Sudoku/Sudoku.txt", "w")
    for i in range(9):
        for j in range(9):
            fichier.write(str(sudoku[i][j]))
        fichier.write("\n")
    fichier.close()
    return readSudoku()


def readSudoku():
    """
    Lit la grille du fichier texte
    :return: sudoku: array
    """
    sudoku = np.zeros((9, 9), int)
    try:
        fichier = open("../Sudoku/Sudoku.txt", "r")
        for i in range(9):
            ligne = fichier.readline()
            j = 0
            for s in ligne:
                try:
                    sudoku[i][j] = int(s)
                    j += 1
                except ValueError: pass
        fichier.close()
    except IOError:
        pass
    return sudoku
