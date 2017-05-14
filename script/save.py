# !usr/bin/env python3
# -*- coding: utf-8 -*-

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
        filename = "../sudoku/Sudoku" + str(nb) + ".txt"
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
    if not filename: filename = "../sudoku/" + getLastFile()
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
    files = os.listdir("../sudoku")
    n = 0
    for files_name in files:
        i = "0"
        for l in files_name:
            try:
                if l.isnumeric(): i += l
            except AttributeError:
                if l.isdigit(): i += l
        if int(i) > n: n = int(i)
    return n + 1


def getLastFile():
    files = os.listdir("../sudoku")
    if files:
        return files[-1]
    else:
        return None


def sudokuToString(sudoku):
    """
    Transform a np.array into a str
    :param sudoku: np.array
    :return: str
    """
    s = ""
    for i in range(9):
        for j in range(9):
            s += str(sudoku[i][j])
        s += "\n"
    return s


def stringToSudoku(string):
    sudoku = np.zeros((9, 9), int)
    for i in range(9):
        for j in range(9):
            sudoku[i, j] = int(string.split()[i][j])
    return sudoku
