import pygame
from pygame.locals import *
import time

import step_motor as spm


def moveMotor(motor, x):
    if x < -1: x = -1
    if abs(x) >= 0.01:
        speed = (((1 - abs(x)) * 400) // 20 + 1) * 20
        direction = int(x / abs(x))
        motor.move, motor.direction, motor.speed = True, direction, speed
    else:
        motor.move = False


pygame.init()
power = 1

bobines_motor1 = (35, 37, 36, 38)
bobines_motor2 = (21, 23, 22, 24)
motor1 = spm.ManualMotor(bobines_motor1)
motor2 = spm.ManualMotor(bobines_motor2)


nb_joystick = pygame.joystick.get_count()
print("il y a {} joystick(s) branché(s)".format(nb_joystick))

if nb_joystick > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Axes :", joystick.get_numaxes())
    print("Boutons :", joystick.get_numbuttons())
    print("Trackballs :", joystick.get_numballs())
    print("Hats :", joystick.get_numhats())

x1 = 0
x2 = 0

motor1.start()
motor2.start()

while power:
    pygame.time.Clock().tick(10)
    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            if event.button == 11:
                motor1.power = False
                motor2.power = False
                power = 0
        if event.type == JOYAXISMOTION:
            if event.axis == 0: x2 = event.value
            if event.axis == 2: x1 = event.value

            if x1 < -1: x1 = -1
            if x2 < -1: x2 = -1

            moveMotor(motor1, x1)
            moveMotor(motor2, x2)