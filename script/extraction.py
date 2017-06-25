# -*- coding: utf-8 -*-
# !usr/bin/env python


import numpy as np
import cv2
import commands
from save import saveSudoku


def rectify(h):
    """
    biggest représente les coordonnées des coins du sudoku
    :param h:
    :return:
    """
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h, axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew


def digit():
    dig = 0
    k = 0
    kernel = np.ones((2, 2), np.uint8)
    decou = cv2.imread('../pictures/Traitement/decoup.jpg')
    decou = cv2.cvtColor(decou, cv2.COLOR_BGR2GRAY)
    decou = cv2.GaussianBlur(decou, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(decou, 255, 1, 1, 11, 2)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    while thresh[0, 0] > 220:
        l = len(thresh)
        thresh = thresh[1:l, 1:l]
    while thresh[len(thresh[0]) - 1, len(thresh[0]) - 1] > 220:
        l = len(thresh[0]) - 1
        thresh = thresh[0:l, 0:l]
    while thresh[0, len(thresh[0]) - 1] > 220:
        l = len(thresh[0])
        thresh = thresh[1:l, 0:l - 1]
    while thresh[len(thresh) - 1, 0] > 220:
        l = len(thresh) - 1
        thresh = thresh[0:l - 1, 1:l]

    cv2.imwrite('../pictures/Traitement/minithresh.jpg', thresh)
    dig = commands.getoutput("gocr -C \"123456789\" ../pictures/Traitement/minithresh.jpg")
    dig = str(dig)
    if len(dig) == 0:
        dig = 0
    else:
        for k in range(len(dig)):
            try:
                dig = int(dig)
            except ValueError:
                dig = 0
    return dig


image_sudoku_original = cv2.imread('../pictures/Sudoku.jpg')
image_sudoku_gray = cv2.cvtColor(image_sudoku_original, cv2.COLOR_BGR2GRAY)
image_sudoku_gray = cv2.GaussianBlur(image_sudoku_gray, (5, 5), 0)
thresh = cv2.adaptiveThreshold(image_sudoku_gray, 255, 1, 1, 11, 2)
item, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
biggest = None
max_zone = 0
for i in contours:
    zone = cv2.contourArea(i)
    if zone > 100:
        peri = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.02 * peri, True)
        if zone > max_zone and len(approx) == 4:
            biggest = approx
            max_zone = zone
            best_cnt = i

approx = rectify(biggest)

h = np.array([[0, 0], [453, 0], [453, 453], [0, 453]], np.float32)

retval = cv2.getPerspectiveTransform(approx, h)
warp = cv2.warpPerspective(image_sudoku_gray, retval, (454, 454))
warp = warp[1:452, 1:452]
sudoku = np.zeros((9, 9), int)


for i in range(0, 9):
    for j in range(0, 9):
        decoup = warp[i * 50 + 4:(i + 1) * 50 - 4, j * 50 + 4:(j + 1) * 50 - 4]
        a = str(i)
        b = str(j)
        c = 'decoup' + a + 'et' + b + '.jpg'
        cv2.imwrite('../pictures/Traitement/decoup.jpg', decoup)
        cv2.imwrite('../pictures/Traitement/' + c, decoup)
        sudoku[i][j] = digit()

cv2.imwrite('../pictures/Traitement/warp.jpg', warp)

print(sudoku)
saveSudoku(sudoku, "/home/pi/Desktop/Sudoku-Plotter/sudoku/Sudoku.txt")
