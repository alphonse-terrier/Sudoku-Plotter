#!/usr/bin/env python3

import numpy as np
from time import time


class Resolution:
    """
    Classe permettant de résoudre un sudoku grâce à différentes méthodes, à savoir :
        - inclusion
        - exclusion
        - bactracking
        - ...
    Si le sudoku n'est pas résoluble, lève une erreur
    """

    def __init__(self, boss):
        self.boss = boss
        self.taille = self.boss.taille
        self.nb_cases = self.boss.nb_cases
        self.methode_resolution = None
        self.vitesse = None
        self.sudoku = np.zeros((self.nb_cases, self.nb_cases), int)
        self.liste_sudoku = []
        self.liste_position = []
        self.power = True

    def start(self, sudoku, methode, vitesse=None):
        self.sudoku = sudoku
        self.methode_resolution = methode
        self.vitesse = vitesse
        print(self.methode_resolution)
        zero_time = time()
        if not self.checkBeforeStart():
            self.boss.setError("sudoku_insoluble")
            return self.sudoku, []
        if self.methode_resolution == "Globale": self.optimale()
        elif self.methode_resolution == "Inclusion": self.inclusion()
        elif self.methode_resolution == "Exclusion": self.exclusion()
        elif self.methode_resolution == "Backtracking":
            self.createListe()
            self.backTracking()
        else: print("La méthode n'est pas reconnue")
        print(time() - zero_time, '\n')
        return np.copy(self.sudoku), self.liste_position

    def checkBeforeStart(self):
        for i in range(self.nb_cases):
            liste_ligne = []
            liste_colonne = [] 
            liste_carre = []
            x = 3 * (i // 3)
            y = 3 * (i % 3)
            for j in range(self.nb_cases):
                if self.sudoku[x + j // 3, y + j % 3] in liste_carre \
                        or self.sudoku[j, i] in liste_colonne \
                        or self.sudoku[i, j] in liste_ligne:
                    return False
                if self.sudoku[i, j] != 0:
                    liste_ligne.append(self.sudoku[i, j])
                if self.sudoku[j, i] != 0:
                    liste_colonne.append(self.sudoku[j, i])
                if self.sudoku[x + j // 3, y + j % 3] != 0:
                    liste_carre.append(self.sudoku[x + j // 3, y + j % 3])
        return True
            
    def createListe(self):
        self.liste_position = []
        liste_tailles_cases_vides = []
        liste_tailles = [[] for i in range(self.nb_cases - 1)]
        for x in range(self.nb_cases):
            for y in range(self.nb_cases):
                if not self.sudoku[x][y]:
                    self.liste_position.append((x, y))
                    liste_tailles_cases_vides.append(len(self.checkListe(x, y)))
                    liste_tailles[liste_tailles_cases_vides[-1] - 2].append((x, y))
        liste_position = []
        for i in range(self.nb_cases - 1):
            liste_position += liste_tailles[i]
        return liste_position

    def checkListe(self, x, y):
        """
        Renvoie la liste des valeurs possibles pour la case de coordonnées x et y
        :param x: int: ligne
        :param y: int: colonne
        :return: liste: list
        """
        liste = []
        if self.sudoku[x][y] == 0:
            liste = [i + 1 for i in range(self.nb_cases)]
            block_x = x - x % self.taille[0]
            block_y = y - y % self.taille[1]
            for i in range(self.nb_cases):
                if self.sudoku[x, i] in liste:
                    liste.remove(self.sudoku[x, i])
                if self.sudoku[i, y] in liste:
                    liste.remove(self.sudoku[i, y])
                if self.sudoku[block_x + i % self.taille[1], block_y + i // self.taille[0]] in liste:
                    liste.remove(self.sudoku[block_x + i % self.taille[1], block_y + i // self.taille[0]])
        return liste

    def optimale(self):
        self.liste_position = self.createListe()
        size = []
        for x, y in self.liste_position:
            size.append(len(self.checkListe(x, y)))
        self.backTracking()

    def inclusion(self):
        pass

    def exclusion(self):
        pass

    def backTracking(self):
        """
        Résoud un sudoku selon la méthode de backtracking
        :return: None or -1
        """
        self.liste_sudoku = []
        i = 0
        while self.power:
            x, y = self.liste_position[i]
            liste = self.checkListe(x, y)
            if liste:
                self.sudoku[x][y] = liste.pop(0)
                self.liste_sudoku.append(liste)
                i += 1
            else:
                while not liste:
                    i -= 1
                    x, y = self.liste_position[i]
                    try:
                        liste = self.liste_sudoku[i]
                    except IndexError:
                        self.sudoku = self.boss.sudoku
                        self.boss.setError("sudoku_insoluble")
                        return -1
                    if liste:
                        self.sudoku[x][y] = liste.pop(0)
                        self.liste_sudoku[i] = liste
                        i += 1
                        break
                    else:
                        self.liste_sudoku.pop(i)
                        self.sudoku[x][y] = 0
            if i < len(self.liste_position):
                self.power = False
        self.power = True



if __name__ == '__main__':
    class Boss:
        def __init__(self):
            self.taille = (3, 3)
            self.nb_cases = 9
            self.methode = 'Globale'
            self.vitesse = 'Pas à Pas'
            self.sudoku = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 2],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 3],
                                    [0, 0, 2, 3, 0, 0, 4, 0, 0],
                                    [0, 0, 1, 8, 0, 0, 0, 0, 5],
                                    [0, 6, 0, 0, 7, 0, 8, 0, 0],
                                    [0, 0, 0, 0, 0, 9, 0, 0, 0],
                                    [0, 0, 8, 5, 0, 0, 0, 0, 0],
                                    [9, 0, 0, 0, 4, 0, 5, 0, 0],
                                    [4, 7, 0, 0, 0, 6, 0, 0, 0]])
            self.Resolution = Resolution(self)
            self.Resolution.start(self.sudoku, self.methode, self.vitesse)
            print(self.sudoku, '\n')

        def setError(self, error):
            if error == "sudoku_insoluble":
                print("Le sudoku n'est pas résoluble")


    Boss()
