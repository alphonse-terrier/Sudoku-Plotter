#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import save
import write as w
import step_motor as stp


def writeSudoku(sudoku):
    points = W.writeSudoku(sudoku)
    while InitMoveMotor.getPoints():
        time.sleep(0.1)
    InitMoveMotor.setPoins(points)
    InitMoveMotor.movingMotor()
    InitMoveMotor.stop()


W = w.Write()
test = True
sudoku = save.readSudoku()
if test:
    W.writeSudoku(sudoku)
    W.write()
else:
    InitMoveMotor = stp.InitMoveMotor()
    writeSudoku(sudoku)