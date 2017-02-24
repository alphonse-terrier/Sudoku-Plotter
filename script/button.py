import RPi.GPIO as GPIO
import threading
import time

import lcd3


class Button:
    number = 0
    def __init__(self, pin):
        self.pin = pin
        self.number = Button.number
        GPIO.setup(self.pin, GPIO.IN)
        Button.number += 1


class Buttons(threading.Thread):
    def __init__(self, bouton_pin):
        threading.Thread.__init__(self)
        GPIO.setmode(GPIO.BOARD)
        self.power = True
        self.pressed = [0 for i in range(len(bouton_pin))]
        self.liste = []
        self.pins = bouton_pin

        for i in self.pins:
            self.liste.append(Button(i))

    def run(self):
        while self.power:
            for i in range(len(self.liste)):
                if GPIO.input(self.liste[i].pin):
                    self.pressed[i] = 1
            time.sleep(2)

    def stop(self):
        self.power = False


if __name__ == "__main__":
    bt = Buttons([11, 13, 15])
    bt.start()
    while True:
        print(bt.pressed)
        time.sleep(1)
