#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt


class Write:
    """
    Classe permettant la creation de chiffres de différentes tailles
    Les chiffres sont constitues b'une succession de coordonnees
    """

    def __init__(self):
        self.points = []
        self.step = 0.02  # 0.0017
        self.coordinate = [(0.5, 0.5), (18.5, 18.5)]
        self.a, self.b = self.coordinate[0][0], self.coordinate[0][1]
        self.c, self.d = self.coordinate[1][0], self.coordinate[1][1]
        self.nx = (self.c - self.a) / 9
        self.ny = (self.d - self.b) / 9
        self.x0 = self.a + self.nx / 2
        self.y0 = self.b + self.ny / 2
        self.L = 2 / 3 * min(self.nx, self.ny)

    def append(self, liste_x, liste_y, x0, y0):
        for i in range(len(liste_x)):
            self.points.append((liste_x[i] + x0, liste_y[i] + y0))

    def writeOne(self, x0, y0):
        x = - self.L / 12
        while x <= self.L / 12:
            y = x + 5 * self.L / 12
            self.points.append((x + x0, y + y0))
            x += self.step
        x = self.L / 12
        y = self.L / 2
        while y >= - self.L / 2:
            self.points.append((x + x0, y + y0))
            y -= self.step
        self.points.append((x0 + self.L / 12, y0 - self.L / 2))
        self.points.append("up")
        x = - self.L / 12
        y = - self.L / 2
        self.points.append("up")
        while x < self.L / 4:
            self.points.append((x + x0, y + y0))
            x += self.step
        self.points.append((self.L / 4 + x0, y + y0))

    def writeTwo(self, x0, y0):
        liste_x, liste_y = [], []
        y = self.L / 8
        x = -10
        while y < 3 * self.L / 7:
            try:
                x = - math.sqrt((self.L / 4) ** 2 - (y - self.L / 4) ** 2)
            except ValueError:
                x = 0
            liste_x.append(x)
            liste_y.append(y)
            y += self.step
        # liste_x.append(- self.L / 4)
        # liste_y.append(self.L / 4)
        while x <= 0:
            y = self.L / 4 + math.sqrt((self.L / 4) ** 2 - x ** 2)
            liste_x.append(x)
            liste_y.append(y)
            x += self.step
        liste_x.append(0)
        liste_y.append(self.L / 2)
        l = len(liste_x)
        for i in range(l - 1, -1, -1):
            liste_x.append(- liste_x[i])
            liste_y.append(liste_y[i])
        x, y = liste_x[-1], liste_y[-1]
        a = (5 * self.L / 8) / (x + self.L / 4)
        b = self.L / 2 * (a / 2 - 1)
        x -= self.step
        while x > - self.L / 4:
            y = a * x + b
            liste_x.append(x)
            liste_y.append(y)
            x -= self.step
        x = - self.L / 4
        y = - self.L / 2
        while x < self.L / 4:
            liste_x.append(x)
            liste_y.append(y)
            x += self.step
        liste_x.append(self.L / 4)
        liste_y.append(y)
        self.append(liste_x, liste_y, x0, y0)

    def writeThree(self, x0, y0):
        liste_x, liste_y = [], []
        y = 0
        x = 0
        while x < self.L / 6:
            y = self.L / 4 + math.sqrt((self.L / 4) ** 2 - x ** 2)
            liste_y.append(y)
            liste_x.append(x)
            x += self.step
        while y >= self.L / 4:
            x = math.sqrt((self.L / 4) ** 2 - (y - self.L / 4) ** 2)
            liste_x.append(x)
            liste_y.append(y)
            y -= self.step
        l = len(liste_x)
        if self.L / 4 not in liste_x or self.L / 4 not in liste_y:
            liste_x.append(self.L / 4)
            liste_y.append(self.L / 4)
        for i in range(l - 1, -1, -1):
            if liste_x[i] > 0:
                liste_x.append(liste_x[i])
                liste_y.append(self.L / 2 - liste_y[i])
        liste_x.append(0)
        liste_y.append(0)
        l = len(liste_x)
        for i in range(l):
            if liste_y[2 * i] < self.L / 3:
                break
            liste_x.insert(0, - liste_x[2 * i])
            liste_y.insert(0, liste_y[2 * i])
        l = len(liste_x)
        for i in range(l):
            liste_x.append(liste_x[l - i - 1])
            liste_y.append(-liste_y[l - 1 - i])
        l = len(liste_x)
        for i in range(l):
            self.points.append((liste_x[i] + x0, liste_y[i] + y0))

    def writeFour(self, x0, y0):
        x, y = self.L / 12, self.L / 2
        while x < self.L / 4:
            self.points.append((x + x0, y + y0))
            if y > - self.L / 6:
                y -= self.step
                x = y / 2 - self.L / 6
            else:
                x += self.step
        self.points.append((self.L / 4 + x0, y + y0))
        self.points.append("up")
        x, y = self.L / 12, 0
        while y > - self.L / 2:
            self.points.append((x + x0, y + y0))
            y -= self.step
        self.points.append((x + x0, - self.L / 2 + y0))

    def writeFive(self, x0, y0):
        x, y = self.L / 4, self.L / 2
        y1 = - self.L / 6 + self.L * math.sqrt(1 / 12)
        while y > y1:
            self.points.append((x + x0, y + y0))
            if x > - self.L / 4:
                x -= self.step
            else:
                y -= self.step
        liste_x, liste_y = [], []
        while x < self.L / 6:
<<<<<<< HEAD
            try:
                y = - self.L / 6 + math.sqrt(self.L ** 2 / 9 - (x + self.L / 12) ** 2)
                liste_x.append(x)
                liste_y.append(y)
            except ValueError:
                pass
=======
            y = - self.L / 6 + math.sqrt(abs(self.L ** 2 / 9 - (x + self.L / 12) ** 2))
            liste_x.append(x)
            liste_y.append(y)
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
            x += self.step
        while y > - self.L / 6:
            x = - self.L / 12 + math.sqrt(self.L ** 2 / 9 - (y + self.L / 6) ** 2)
            liste_x.append(x)
            liste_y.append(y)
            y -= self.step
        l = len(liste_x)
        for i in range(l):
            liste_x.append(liste_x[l - 1 - i])
            liste_y.append(-self.L / 3 - liste_y[l - 1 - i])
        l = len(liste_x)
        for i in range(l):
            self.points.append((liste_x[i] + x0, liste_y[i] + y0))

    def writeSix(self, x0, y0):
        x, y = self.L / 5, self.L / 2
        while x > - self.L / 6:
            y = self.L / 6 + math.sqrt(self.L ** 2 / 9 - (x - self.L / 12) ** 2)
            self.points.append((x + x0, y + y0))
            x -= self.step
        while y > self.L / 6:
            x = self.L / 12 - math.sqrt(self.L ** 2 / 9 - (y - self.L / 6) ** 2)
            self.points.append((x + x0, y + y0))
            y -= self.step
        x = - self.L / 4
        while y > - self.L / 4:
            self.points.append((x + x0, y + y0))
            y -= self.step
        liste_x, liste_y = [], []
        while x < - self.L / 6:
            try:
                x = - math.sqrt(self.L ** 2 / 16 - (y + self.L / 4) ** 2)
            except ValueError:
                x = 0
                y = 0
            liste_x.append(x)
            liste_y.append(y)
            y -= self.step
        while x <= 0:
            y = - self.L / 4 - math.sqrt(self.L ** 2 / 16 - x ** 2)
            liste_x.append(x)
            liste_y.append(y)
            x += self.step
        l = len(liste_x)
        liste_x.append(0)
        liste_y.append(-self.L / 2)
        for i in range(l - 1, -1, -1):
            liste_x.append(- liste_x[i])
            liste_y.append(liste_y[i])
        liste_x.append(self.L / 4)
        liste_y.append(-self.L / 4)
        l = len(liste_x)
        for i in range(l - 1, -1, -1):
            liste_x.append(liste_x[i])
            liste_y.append(- self.L / 2 - liste_y[i])
        self.append(liste_x, liste_y, x0, y0)

    def writeSeven(self, x0, y0):
        x = - self.L / 4
        y = self.L / 2
        while x <= self.L / 4:
            self.points.append((x + x0, y + y0))
            x += self.step
        while y >= - self.L / 2:
            x = y / 2
            self.points.append((x + x0, y + y0))
            y -= self.step
        self.points.append((-self.L / 4 + x0, -self.L / 2 + y0))

    def writeEight(self, x0, y0):
        liste_x, liste_y = [], []
        y = 0
        x = 0
        while x < self.L / 6:
            y = self.L / 4 + math.sqrt((self.L / 4) ** 2 - x ** 2)
            liste_y.append(y)
            liste_x.append(x)
            x += self.step
        while y >= self.L / 4:
            x = math.sqrt((self.L / 4) ** 2 - (y - self.L / 4) ** 2)
            liste_x.append(x)
            liste_y.append(y)
            y -= self.step
        l = len(liste_x)
        if self.L / 4 not in liste_x or self.L / 4 not in liste_y:
            liste_x.append(self.L / 4)
            liste_y.append(self.L / 4)
        for i in range(l - 1, -1, -1):
            if liste_x[i] > 0:
                liste_x.append(liste_x[i])
                liste_y.append(self.L / 2 - liste_y[i])
        liste_x.append(0)
        liste_y.append(0)
        l = len(liste_x)
        for i in range(l):
            if liste_y[2 * i] < 0:
                break
            liste_x.insert(0, - liste_x[2 * i])
            liste_y.insert(0, liste_y[2 * i])
        l = len(liste_x)
        for i in range(l):
            liste_x.append(liste_x[i])
            liste_y.append(-liste_y[i])
        l = len(liste_x)
        liste_x += [0]
        liste_y += [0]
        while x < self.L / 6:
            y = self.L / 4 + math.sqrt((self.L / 4) ** 2 - x ** 2)
            liste_y.append(y)
            liste_x.append(x)
            x += self.step
        for i in range(l):
            self.points.append((liste_x[l - 1 - i] + x0, liste_y[l - 1 - i] + y0))

    def writeNine(self, x0, y0):
        x = y = self.L / 4
        liste_x, liste_y = [], []
        while x > self.L / 6:
            try:
                x = math.sqrt(self.L ** 2 / 16 - (y - self.L / 4) ** 2)
            except ValueError:
                x = 0
                y = 0
            liste_x.append(x)
            liste_y.append(y)
            y += self.step
        while x >= 0:
            y = self.L / 4 + math.sqrt(self.L ** 2 / 16 - x ** 2)
            liste_x.append(x)
            liste_y.append(y)
            x -= self.step
        l = len(liste_x)
        liste_x.append(0)
        liste_y.append(self.L / 2)
        for i in range(l - 1, -1, -1):
            liste_x.append(- liste_x[i])
            liste_y.append(liste_y[i])
        liste_x.append(- self.L / 4)
        liste_y.append(self.L / 4)
        l = len(liste_x)
        for i in range(l - 1, -1, -1):
            liste_x.append(liste_x[i])
            liste_y.append(self.L / 2 - liste_y[i])
<<<<<<< HEAD
=======
        l = len(liste_x)
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
        liste_x.reverse()
        liste_y.reverse()
        self.append(liste_x, liste_y, x0, y0)
        x = y = self.L / 4
        while y > - self.L / 6:
            self.points.append((x + x0, y + y0))
            y -= self.step
        while x > self.L / 5:
<<<<<<< HEAD
            try:
                x = - self.L / 12 + math.sqrt(abs(self.L ** 2 / 9 - (y + self.L / 6) ** 2))
                self.points.append((x + x0, y + y0))
            except ValueError: pass
=======
            x = - self.L / 12 + math.sqrt(abs(self.L ** 2 / 9 - (y + self.L / 6) ** 2))
            self.points.append((x + x0, y + y0))
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
            y -= self.step
        while x >= - self.L / 5:
            y = - self.L / 6 - math.sqrt(self.L ** 2 / 9 - (x + self.L / 12) ** 2)
            self.points.append((x + x0, y + y0))
            x -= self.step

    def writeNumbers(self, n, x0, y0):
        if n == 1:
            self.writeOne(x0, y0)
        elif n == 2:
            self.writeTwo(x0, y0)
        elif n == 3:
            self.writeThree(x0, y0)
        elif n == 4:
            self.writeFour(x0, y0)
        elif n == 5:
            self.writeFive(x0, y0)
        elif n == 6:
            self.writeSix(x0, y0)
        elif n == 7:
            self.writeSeven(x0, y0)
        elif n == 8:
            self.writeEight(x0, y0)
        elif n == 9:
            self.writeNine(x0, y0)
        else:
            return 0
        self.points.append("up")

    def writeLine(self, x0, y0, x1, y1):
        x = x0
        if x1 == x0:
            y = y0
            if y0 < y1:
                while y < y1:
                    self.points.append((x, y))
<<<<<<< HEAD
                    y += self.step / 15
            else:
                while y > y1:
                    self.points.append((x, y))
                    y -= self.step / 15
=======
                    y += self.step * 10
            else:
                while y > y1:
                    self.points.append((x, y))
                    y -= self.step * 10
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
        else:
            a = (y1 - y0) / (x1 - x0)
            b = y0 - a * x0
            if x0 < x1:
                while x < x1:
                    y = a * x + b
                    self.points.append((x, y))
<<<<<<< HEAD
                    x += self.step / 15
=======
                    x += self.step * 10
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
            else:
                while x > x1:
                    y = a * x + b
                    self.points.append((x, y))
<<<<<<< HEAD
                    x -= self.step / 15
=======
                    x -= self.step * 10
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
        self.points.append((x1, y1))
        self.points.append("up")

    def writeSudoku(self, sudoku):
        self.points.insert(0, "up")
        for i in range(10):
            if i % 2:
                self.writeLine(self.c, self.b + self.ny * i, self.a, self.b + self.ny * i)
            else:
                self.writeLine(self.a, self.b + self.ny * i, self.c, self.b + self.ny * i)
        for i in range(10):
            if i % 2:
                self.writeLine(self.a + self.nx * i, self.b, self.a + self.nx * i, self.d)
            else:
                self.writeLine(self.a + self.nx * i, self.d, self.a + self.nx * i, self.b)
        for i in range(9):
            for j in range(9):
                if i % 2:
                    if sudoku[i][j]:
                        self.writeNumbers(sudoku[i][j], self.x0 + self.nx * j,
                                          self.y0 + self.ny * (8 - i))
                else:
                    if sudoku[i][8 - j]:
                        self.writeNumbers(sudoku[i][8 - j], self.x0 + self.nx * (8 - j),
                                          self.y0 + self.ny * (8 - i))
        s = 0
        for i in range(len(self.points) - 1):
            if self.points[i + s] == "up":
                self.points.insert(i + s + 2, "down")
                s += 1
        self.points.insert(1, "down")
        return self.points

    def writeAllNumbers(self):
        self.L = 1
        for i in range(10):
            self.writeNumbers(i, 4 / 5 * i * self.L, 0)

    def write(self, linked=False):
        x, y = [], []
        for point in self.points:
            if point != "up" and point != "down":
                x.append(point[0])
                y.append(point[1])
        if linked:
            plt.plot(x, y, 'r', linewidth=2)
        else:
            plt.scatter(x, y, c='red', s=8)
        plt.grid(True)
        plt.axis('equal')
        # plt.axis('off')
        plt.show()


if __name__ == "__main__":
    w = Write()
    sudoku = np.array([[0, 0, 0, 0, 0, 0, 0, 1, 2],
                       [0, 0, 0, 0, 0, 0, 0, 0, 3],
                       [0, 0, 2, 3, 0, 0, 4, 0, 0],
                       [0, 0, 1, 8, 0, 0, 0, 0, 5],
                       [0, 6, 0, 0, 7, 0, 8, 0, 0],
                       [0, 0, 0, 0, 0, 9, 0, 0, 0],
                       [0, 0, 8, 5, 0, 0, 0, 0, 0],
                       [9, 0, 0, 0, 4, 0, 5, 0, 0],
                       [4, 7, 0, 0, 0, 6, 0, 0, 0]])
    """w.writeAllNumbers()
    for i in w.points: print(i)
    w.write(True)
    """
    # for i in w.writeSudoku(sudoku): print(i)
    w.writeOne(0, 0)
    print(w.points)
    w.write()
