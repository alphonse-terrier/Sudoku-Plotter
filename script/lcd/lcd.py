#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
# import lcddriver


class Lcd:
    def __init__(self):
        self.power = True
        self.text = ["", ""]
        self.previous_text = ["", ""]
        # self.display = lcddriver.Lcd()

    def start(self):
        open("text.txt", "w").close()
        open("previous_text.txt", "w").close()
        while self.power:
            self.write()
            time.sleep(0.1)

    def write(self):
        try:
            text = open("text.txt", 'r')
            previous_text = open("previous_text.txt", 'r')
            for i in range(2):
                self.text[i] = text.readline().replace('\n', '')
                self.previous_text[i] = previous_text.readline().replace('\n', '')
                if self.text[i] != self.previous_text[i]:
                    self.writeLine(self.text[i].center(16), i)
            text.close()
            previous_text.close()
        except IOError:
            pass
        if self.text != self.previous_text:
            previous_text = open("previous_text.txt", "w")
            previous_text.write(self.text[0] + '\n' + self.text[1])
            previous_text.close()

    def writeLine(self, text, i):
        print(text)
        # self.display.lcd_dislplay_string(text, i)

    def close(self):
        self.power = False
        # self.display.lcd_clear()


Lcd().start()
