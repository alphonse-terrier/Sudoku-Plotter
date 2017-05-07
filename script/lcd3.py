#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def configure(text):
    text = text.strip()
    if len(text) < 16:
        return [text, ""]
    else:
        n = 15
        for i in range(16):
            if text[i].isspace(): n = i
        new_text = [text[:n].strip(), text[n:].strip()]
        if len(new_text[1]) > 16:
            new_text = [text[:16], text[16:]]
        return new_text


def write(text):
    text = configure(text)
    os.chdir("/home/pi/Desktop/Sudoku-Plotter/script/lcd")
    file = open("text.txt", "w")
    file.write(text[0] + '\n' + text[1])
    file.close()
