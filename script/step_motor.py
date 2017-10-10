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
    déplace les moteurs simultanément pour se rendre b'un point à un autre
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
        self.max_speed1 = 10
        self.max_speed2 = 60
        self.r_step = 0.0203
        self.theta_step = 0.0056
        self.speed1 = []
        self.speed2 = []
        self.nb_steps1 = []
        self.nb_steps2 = []
        self.pen_position = []
        self.points = []

        self.pinInit()

        self.motor1 = Motor(self.bobines_motor1)
        self.motor2 = Motor(self.bobines_motor2)
        self.servoMotor = ServoMotor(self.pwm_servo)
        self.setMicroStep()

        self.motor1.start()
        self.motor2.start()

    def run(self):
        while self.power:
            if self.points:
                self.moveMotor()
            time.sleep(0.1)
	
    def initializePosition(self):
        self.motor1.initializePosition()

    def moveMotor(self):
        points = []
        for i in range(len(self.points)):
            if self.points[i] != "up" and self.points[i] != "down":
                x, y = self.points[i]
                B = Point(x, y)
                points.append(self.points[i])
                r = B.r - self.M.r
                theta = B.theta - self.M.theta
                self.nb_steps1.append(int(r / self.r_step + 0.5))
                self.nb_steps2.append(int(theta / self.theta_step + 0.5))
                self.setTime()
                self.M = Point(self.M.r + self.nb_steps1[-1] * self.r_step,
                               self.M.theta + self.nb_steps2[-1] * self.theta_step, "polar")
            else:
                self.pen_position.append((self.points[i], i))
        self.points = []
        for i in range(len(self.nb_steps1)):
            if self.points[i] != "up" and self.points[i] != "down":
                self.motor1.nb_steps = self.nb_steps1[i]
                self.motor2.nb_steps = self.nb_steps2[i]
                self.motor1.speed = self.speed1[i]
                self.motor2.speed = self.speed2[i]
            else:
                self.servoMotor.setServo(self.points[0])
            while self.motor1.nb_steps != 0 or self.motor2.nb_steps != 0:
                time.sleep(0.0001)
        self.sleep()

    def setTime(self):
        if not self.nb_steps1[-1]:
            self.speed1.append(0)
            self.speed2.append(self.max_speed2)
        elif not self.nb_steps2[-1]:
            self.speed1.append(self.max_speed1)
            self.speed2.append(0)
        else:
=======
        current_pen_position = 0
        for i in range(len(self.points)):
            if self.points[i] != "up" and self.points[i] != "down": 
                self.motor1.nb_steps = self.nb_steps1[i - current_pen_position]
                self.motor2.nb_steps = self.nb_steps2[i - current_pen_position]
                self.motor1.speed = self.speed1[i - current_pen_position]
                self.motor2.speed = self.speed2[i - current_pen_position]
            else:
                self.servoMotor.setServo(self.points[i])
                current_pen_position += 1
            while self.motor1.nb_steps != 0 or self.motor2.nb_steps != 0:
                time.sleep(0.0001)
        self.nb_steps1 = self.nb_steps2 = []
        self.speed1 = self.speed2 = []
        if len(self.points) > 1: 
            self.clearUp()
        else:
            self.sleep()

    def setTime(self):
        if not self.nb_steps1[-1]:
            self.speed1.append(0)
            self.speed2.append(self.max_speed2)
        elif not self.nb_steps2[-1]:
            self.speed1.append(self.max_speed1)
            self.speed2.append(0)
        else:
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
            total_time1 = abs(self.max_speed1 * self.nb_steps1[-1])
            total_time2 = abs(self.max_speed2 * self.nb_steps2[-1])
            if (total_time1 > total_time2 and abs(total_time2 / self.nb_steps1[-1]) > self.max_speed1) or abs(
                            total_time1 / self.nb_steps2[-1]) < self.max_speed2:
                total_time = total_time2
            else:
                total_time = total_time1
            self.speed1.append(abs(total_time / self.nb_steps1[-1]))
            self.speed2.append(abs(total_time / self.nb_steps2[-1]))

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

    def setMicroStep(self):
        micro_step = min(self.motor1.micro_step, self.motor2.micro_step)
        self.max_speed1 = self.max_speed1 / micro_step
        self.max_speed2 = self.max_speed2 / micro_step
        self.r_step /= self.motor1.micro_step
        self.theta_step /= self.motor2.micro_step

    def setPoints(self, points):
        self.points = points

    def getPoints(self):
        return self.points

    def clearUp(self):
<<<<<<< HEAD
        B = Point(-7.5, 12)
=======
        self.servoMotor.setServo("up")
        B = Point(-7.5, 20)
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2
        r = B.r - self.M.r
        theta = B.theta - self.M.theta
        self.motor1.nb_steps = int(r / self.r_step + 0.5)
        self.motor2.nb_steps = int(theta / self.theta_step + 0.5)
        self.motor2.speed = self.max_speed1
<<<<<<< HEAD
        self.motor1.speed = self.motor2.nb_steps * self.motor2.speed / self.motor1.nb_steps
=======
        self.motor1.speed = abs(self.motor2.nb_steps * self.motor2.speed / self.motor1.nb_steps)
        while self.motor1.nb_steps or self.motor2.nb_steps:
            time.sleep(0.001)
        self.sleep()
>>>>>>> e452e8dd06e839fc6778d2e9119472cb964122a2

    def sleep(self):
        self.points = []
        self.motor1.sleep()
        self.motor2.sleep()

    def stop(self):
        """self.servoMotor.setServo("up")
        self.motor1.stop()
        self.motor2.stop()"""
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
        self.micro_step = 16
        self.number = Motor.nb
        self.bobines = bobines
        self.init_position = 0
        self.position = position
        self.init_position = 0
        self.nb_steps = nb_steps
        self.button_pin = (16, 18)
        self.stop_left = False
        self.stop_right = False
        self.direction = {"left": -1, "right": 1}
        self.PWM = self.initPWM()
        self.motor_alim = self.setMicroStep()

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

    def initPWM(self):
        pwm = []
        for i in range(4):
            pwm.append(GPIO.PWM(self.bobines[i], 1500))
            pwm[i].start(0)
        return pwm

    def setMicroStep(self):
        next = None
        previous = None
        motor_alim = [[1, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0]]
        new_alim = []
        for i in range(4):
            for j in range(4):
                if motor_alim[i][j]: previous = j
                if motor_alim[(i + 1) % 4][j]: next = j
            for j in range(self.micro_step):
                new_alim.append([0, 0, 0, 0])
                new_alim[-1][previous] = 1 - j / self.micro_step
                new_alim[-1][next] = j / self.micro_step
        return new_alim

    def initializePosition(self, direction='left'):
        while not self.bt.pressed[0]:
            self.position += self.direction[direction]
            self.setPins()
            time.sleep(0.01 / self.micro_step)

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
            self.init_position += rotation
            self.setPins()

    def setPins(self):
        if not error:
            for i in range(4):
                self.PWM[i].ChangeDutyCycle(self.motor_alim[self.position % (4 * self.micro_step)][i] * 100)

    def sleep(self):
        print("motor{}: sleep".format(self.number))
        if not error:
            for i in range(4):
                self.PWM[i].ChangeDutyCycle(0)

    def stop(self):
        print("motor{}: stop".format(self.number))
        self.power = False

    def setPower(self, power):
        self.power = power


class ServoMotor:
    def __init__(self, pin):
        self.positions = {'up': 5.5, 'down': 2.1}
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
    init.start()
    """time.sleep(5)
    init.stop()"""
