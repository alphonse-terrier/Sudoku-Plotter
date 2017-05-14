#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

import time
import math
import threading

try:
    error = None
    import button as bt
    import RPi.GPIO as GPIO
except ImportError:
    error = "module_GPIO"


class MotorControl(threading.Thread):
    """
    Vérifie que le module RPI.GPIO permettant de gérer les sorties/entrées GPIO
    de la raspberry a été importé correctement,
    définit les sorties GPIO de la Raspberry utilisées pour controler les moteurs,
    initialise les processus des moteurs (motor1 et motor2),
    déplace les moteurs simultanément pour se rendre d'un point à un autre
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.tryError()
        self.power = True
        self.beta_version = True
        self.bobines_motor1 = (29, 31, 33, 35)
        self.bobines_motor2 = (7, 11, 13, 15)
        self.pwm_servo = 8
        self.turn_on_led = 19
        self.working_led = 21
        self.M = Point(0, 7)
        self.r_step = 0.0203
        self.theta_step = 0.0056
        self.points = []  # ['down', (5, 16), (5, 20), (9, 20), (9, 16), (5, 16), 'up']  # [(22, 7), (16.2, 24.07), (4.3, 14.93)]

        self.pinInit()

        self.motor1 = Motor(self.bobines_motor1)
        self.motor2 = Motor(self.bobines_motor2)
        self.servoMotor = ServoMotor(self.pwm_servo)
        self.turnOnLed = BlinkingLed(self.turn_on_led)
        self.workingLed = BlinkingLed(self.working_led, True)

        self.motor1.start()
        self.motor2.start()
        self.turnOnLed.start()
        self.workingLed.start()

    def run(self):
        while self.power:
            if self.points:
                self.movingMotor()
            time.sleep(0.1)

    def initializePosition(self):
        self.motor1.initializePosition()

    def movingMotor(self):
        self.sleep(False)
        while self.points:
            if self.points[0] == "up" or self.points[0] == "down":
                self.servoMotor.setServo(self.points[0])
            else:
                x_b, y_b = self.points[0]
                B = Point(x_b, y_b)
                r = B.r - self.M.r
                theta = B.theta - self.M.theta
                print(r, theta)
                nb_steps1 = int(r / self.r_step + 0.5)
                nb_steps2 = int(theta / self.theta_step + 0.5)
                print(nb_steps1, nb_steps2)
                if abs(nb_steps1) > abs(nb_steps2):
                    self.motor1.speed, self.motor2.speed = self.setTime(nb_steps1, nb_steps2)
                else:
                    self.motor2.speed, self.motor1.speed = self.setTime(nb_steps2, nb_steps1)
                print(self.motor1.speed, self.motor2.speed)
                self.motor1.nb_steps = nb_steps1
                self.motor2.nb_steps = nb_steps2
                while self.motor1.nb_steps != 0 or self.motor2.nb_steps != 0:
                    time.sleep(0.1)
                self.M = Point(x_b, y_b)
                if self.motor1.stop_left: self.M.r = 7
                elif self.motor1.stop_right: self.M.r = 22
                self.M.newCartesianCoords()
            self.points.pop(0)
        self.sleep()

    def setTime(self, nb_step_a, nb_step_b):
        speed_a = 10
        if nb_step_b != 0:
            speed_b = abs(nb_step_a * speed_a / nb_step_b)
        else:
            speed_b = 0
        return speed_a, speed_b

    def startMoving(self):
        power = True

    def pinInit(self):
        """
        Initialise les pins de la raspberry pour contrôler le moteur
        :return: None
        """
        if not error:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(self.pwm_servo, GPIO.OUT)
            for i in range(4):
                GPIO.setup(self.bobines_motor1[i], GPIO.OUT)
                GPIO.setup(self.bobines_motor2[i], GPIO.OUT)
        else:
            print(error)

    def tryError(self):
        """
        Renvoie une errur le cas échéant
        :return:
        """
        pass

    def setPoints(self, points):
        self.points = points

    def getPoints(self):
        return self.points

    def sleep(self, sleep=True):
        if sleep:
            self.motor1.sleep()
            self.motor2.sleep()
            self.workingLed.sleep()
            self.turnOnLed.sleep(False)
        else:
            self.workingLed.sleep(False)
            self.turnOnLed.sleep()

    def stop(self):
        self.servoMotor.setServo("up")
        self.motor1.stop()
        self.motor2.stop()
        self.workingLed.stop()
        self.turnOnLed.stop()
        if not error: GPIO.cleanup()
        self.power = False


class Motor(threading.Thread):
    """
    Classe permettant de controller les moteurs 
    pas-à-pas indépendamment l'un de l'autre
    """
    nb = 1

    def __init__(self, bobines=0, position=0, nb_steps=0, speed=10):
        threading.Thread.__init__(self)
        self.power = True
        self.speed = speed
        self.number = Motor.nb
        self.bobines = bobines
        self.position = position
        self.nb_steps = nb_steps
        self.button_pin = (16, 18)
        self.stop_left = False
        self.stop_right = False
        self.direction = {"left": -1, "right": 1}
        self.motor_alim = [[1, 0, 0, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0]]

        self.bt = bt.Buttons(self.button_pin)
        self.bt.start()

        Motor.nb += 1

    def run(self):
        while self.power:
            if self.nb_steps != 0:
                time.sleep(self.speed / 1000)
                self.moveMotor()
            else:
                time.sleep(0.1)

    def initializePosition(self, direction='left'):
        while not self.bt.pressed[0]:
            self.position += self.direction[direction]
            self.setPins()
            time.sleep(0.01)

    def moveMotor(self):
        if self.number == 1:
            self.stop_right = self.stop_left = False
            if self.bt.pressed[0] and self.nb_steps < 0:
                self.stop_left = True
                return 0
            if self.bt.pressed[1] and self.nb_steps > 0:
                self.stop_right = True
                return 0
        if self.nb_steps != 0:
            rotation = int(self.nb_steps / abs(self.nb_steps))
            self.nb_steps -= rotation
            self.position += rotation
            self.setPins()

    def setPins(self):
        if not error:
            for i in range(4):
                GPIO.output(self.bobines[i], self.motor_alim[self.position % 4][i])

    def sleep(self):
        print("motor{}: sleep".format(self.number))
        if not error:
            for i in range(4):
                GPIO.output(self.bobines[i], 0)

    def stop(self):
        print("motor{}: stop".format(self.number))
        self.power = False

    def setPower(self, power):
        self.power = power


class ServoMotor:
    def __init__(self, pin):
        self.positions = {'up': 5.5, 'down': 2}
        self.frequency = 50
        self.pin = pin
        self.power = True
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(self.positions['up'])

    def setServo(self, position):
        self.pwm.ChangeDutyCycle(self.positions[position])


class ManualMotor(Motor):
    def __init__(self, bobines, position=0, nb_steps=0, speed=100):
        Motor.__init__(self)
        self.bobines = bobines
        self.position = position
        self.nb_steps = nb_steps
        self.speed = speed
        self.move = False
        self.direction = 1

    def run(self):
        while self.power:
            if self.move:
                time.sleep(self.speed / 1000)
                self.moveMotor()
            else:
                time.sleep(0.1)

    def moveMotor(self):
        self.position += self.direction


class BlinkingLed(threading.Thread):
    def __init__(self, led_pin, sleeping=False):
        threading.Thread.__init__(self)
        self.power = True
        self.sleeping = sleeping
        self.led_pin = led_pin
        self.pinInit()

    def run(self):
        while self.power:
            if self.sleeping or error:
                time.sleep(2)
            else:
                GPIO.output(self.led_pin, 1)
                time.sleep(0.1)
                GPIO.output(self.led_pin, 0)
                time.sleep(1)

    def pinInit(self):
        if not error:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.led_pin, GPIO.OUT)

    def stop(self):
        self.power = False

    def sleep(self, sleeping=True):
        self.sleeping = sleeping


class Origin:
    def __init__(self):
        self.x_0 = -7.5
        self.y_0 = 7

    def coords(self):
        return self.x_0, self.y_0


class Point(Origin):
    def __init__(self, x, y, coordinate="cartesian"):
        Origin.__init__(self)
        if coordinate == "cartesian":
            self.x, self.y = x, y
            self.newPolarCoords()
        else:
            self.r = x
            self.theta = y
            self.newCartesianCoords()

    def newPolarCoords(self):
        self.r = math.sqrt((self.x - self.x_0) ** 2 + (self.y - self.y_0) ** 2)
        if self.y == self.y_0:
            self.theta = 0
        else:
            self.theta = (self.y - self.y_0) / abs(self.y - self.y_0) * math.acos((self.x - self.x_0) / self.r)

    def newCartesianCoords(self):
        self.x = self.r * math.cos(self.theta) + self.x_0
        self.y = self.r * math.sin(self.theta) + self.y_0


if __name__ == "__main__":
    init = MotorControl()
    time.sleep(5)
    init.stop()
