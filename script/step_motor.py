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
        self.sleep_servo = 0.4
        self.up = []
        self.down = []
        self.turn_on_led = 19
        self.working_led = 21
        self.M = Point(0, 7)
        self.max_speed = 0
        self.max_speed1 = 20 / 1000
        self.max_speed2 = 20 / 1000
        self.r_step = 0.0203
        self.theta_step = 0.0056
        self.nb_steps = []
        self.pen_position = []
        self.pinInit()

        self.motor1 = Motor(self.bobines_motor1)
        self.motor2 = Motor(self.bobines_motor2)
        self.servoMotor = ServoMotor(self.pwm_servo)
        self.setMicroStep()
        self.initializePosition()

    def run(self):        
        while self.power:
            self.motor1.checkTime()
            self.motor2.checkTime()
            if not self.motor1.nb_steps and not self.motor2.nb_steps:
                self.writeNextPoints()

    def initializePosition(self):
        self.motor1.initializePosition()

    def writeNextPoints(self):        
        if self.up and not self.up[0]:
            self.servoMotor.setServo("up")
            time.sleep(self.servo_sleep)
            self.up.pop(0)
        elif self.down and not self.down[0]:
            self.servoMotor.setServo("down")
            time.sleep(self.servo_sleep)
            self.down.pop(0)
        else:
            if self.nb_steps:
                self.motor1.nb_steps = self.nb_steps[0][0]
                self.motor2.nb_steps = self.nb_steps[0][1]
                self.nb_steps.pop(0)
                if self.up: self.up[0] -= 1
                if self.down: self.down[0] -= 1
                print(self.nb_steps)
                self.setTime()

    def convertPoints(self, points):
        # <previous_up> (resp. <previous_down>) definissent l'espacement entre deux "up" successifs (resp. "down")
        previous_up = 0
        previous_down = 0

        for i in range(len(points)):
            if points[i] == "up":
                self.up.append(i - previous_up)  # ajout de l'ecart entre deux "up" successifs
                previous_up = i + 1
                previous_down += 1  # permet de ne pas comptabiliser si ce n'est pas un point (ie si point[i] = "up")
            elif points[i] == "down":
                self.down.append(i - previous_down)  # ajout de l'ecart entre deux "down" successifs
                previous_down = i + 1
                previous_up += 1  # permet de ne pas comptabiliser si ce n'est pas un point (ie si point[i] = "down")
            else:
                x, y = points[i]
                B = Point(x, y)
                r = B.r - self.M.r
                theta = B.theta - self.M.theta
                self.nb_steps.append((int(r / self.r_step + 0.5), int(theta / self.theta_step + 0.5)))
                self.M = Point(self.M.r + self.nb_steps[-1][0] * self.r_step,
                               self.M.theta + self.nb_steps[-1][1] * self.theta_step, "polar")

        """for i in range(len(self.points)):
            if self.points[i] != "up" and self.points[i] != "down":
                self.motor1.nb_steps = self.nb_steps1[i]
                self.motor2.nb_steps = self.nb_steps2[i]
                self.motor1.speed = self.speed1[i]
                self.motor2.speed = self.speed2[i]
            else:
                self.servoMotor.setServo(self.points[0])
            while self.motor1.nb_steps != 0 or self.motor2.nb_steps != 0:
                time.sleep(0.0001)"""
        self.sleep()

    def setTime(self):
        """if not self.nb_steps[-1][0]:
            self.motor1.speed.append(0)
            self.motor2.speed.append(self.max_speed2)
        elif not self.nb_steps[-1][1]:
            self.motor1.speed.append(self.max_speed1)
            self.motor2.speed.append(0)
        else:
            total_time1 = abs(self.max_speed1 * self.nb_steps[-1][0])
            total_time2 = abs(self.max_speed2 * self.nb_steps[-1][1])
            if (total_time1 > total_time2 and abs(total_time2 / self.nb_steps[-1][0]) > self.max_speed1) or abs(
                            total_time1 / self.nb_steps[-1][1]) < self.max_speed2:
                total_time = total_time2
            else:
                total_time = total_time1
            self.motor1.speed.append(abs(total_time / self.nb_steps[-1][0]))
            self.motor2.speed.append(abs(total_time / self.nb_steps[-1][1]))"""
    
        if not self.nb_steps[-1][0]:
            self.motor1.speed = 0
            self.motor2.speed = self.max_speed2
        elif not self.nb_steps[-1][1]:
            self.motor1.speed = self.max_speed1
            self.motor2.speed = 0
        else:
            total_time1 = abs(self.max_speed1 * self.nb_steps[-1][0])
            total_time2 = abs(self.max_speed2 * self.nb_steps[-1][1])
            if (total_time1 > total_time2 and abs(total_time2 / self.nb_steps[-1][0]) > self.max_speed1) or abs(
                            total_time1 / self.nb_steps[-1][1]) < self.max_speed2:
                total_time = total_time2
            else:
                total_time = total_time1
            self.motor1.speed = abs(total_time / self.nb_steps[-1][0])
            self.motor2.speed = abs(total_time / self.nb_steps[-1][1])


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
        self.max_speed = self.max_speed / micro_step
        self.r_step /= self.motor1.micro_step
        self.theta_step /= self.motor2.micro_step

    def clearUp(self):
        B = Point(-7.5, 12)
        r = B.r - self.M.r
        theta = B.theta - self.M.theta
        self.motor1.nb_steps = int(r / self.r_step + 0.5)
        self.motor2.nb_steps = int(theta / self.theta_step + 0.5)
        self.motor2.speed = self.max_speed1
        self.motor1.speed = self.motor2.nb_steps * self.motor2.speed / self.motor1.nb_steps

    def sleep(self):
        self.motor1.sleep()
        self.motor2.sleep()

    def stop(self):
        """self.servoMotor.setServo("up")
        self.motor1.stop()
        self.motor2.stop()"""
        if not error: GPIO.cleanup()
        self.power = False


class Motor:
    """
    Classe permettant de controller les moteurs 
    pas-à-pas indépendamment l'un de l'autre
    """
    nb = 1

    def __init__(self, bobines=0, position=0, nb_steps=0, speed=10):
        self.speed = speed
        self.time = 0
        self.micro_step = 2
        self.number = Motor.nb
        self.bobines = bobines
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

    def checkTime(self):
        if self.nb_steps:
            if time.time() - self.time >= self.speed:
                self.moveMotor()
                self.time = time.time()

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
    init.convertPoints([(12, 3), (4, 5), "up", (3, 7), "up", "down"])

