# -*- coding: utf-8 -*-
# !usr/bin/env python

import os
import numpy as np


def saveSudoku(sudoku, filename=None):
    """
    Enregistre la grille dans un fichier texte
    :param filename: 
    :param sudoku:
    :return: None
    """
    if not filename:
        nb = getFileName()
        filename = "../text/Sudoku" + str(nb) + ".txt"
    if ".txt" not in filename:
        filename += '.txt'
    fichier = open(filename, "w")
    for i in range(9):
        for j in range(9):
            fichier.write(str(sudoku[i][j]))
        fichier.write("\n")
    fichier.close()
    return readSudoku()


def readSudoku(filename=None):
    """
    Lit la grille du fichier texte
    :return: sudoku: array
    """
    sudoku = np.zeros((9, 9), int)
    if not filename: filename = "../text/" + getLastFile()
    try:
        fichier = open(filename, "r")
        for i in range(9):
            ligne = fichier.readline()
            j = 0
            for s in ligne:
                try:
                    sudoku[i][j] = int(s)
                    j += 1
                except ValueError:
                    pass
        fichier.close()
    except IndexError:
        sudoku = np.zeros((9, 9), int)
    except IOError:
        pass
    return sudoku


def getFileName():
    files = os.listdir("../text")
    n = 0
    for files_name in files:
        i = "0"
        for l in files_name:
            if l.isnumeric(): i += l
        if int(i) > n: n = int(i)
    return n + 1


def getLastFile():
    files = os.listdir("../text")
    if files:
        return files[-1]
    else:
        return None
