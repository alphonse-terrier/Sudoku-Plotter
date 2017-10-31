#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

##### Stepper Motors #####
r_step = 0.0203
theta_step = 0.0056
micro_step = 8
max_speed1 = 20  # speed max in ms
max_speed2 = 80  # speed max in ms
sleep_servo = 0.4
pwm_frequency = 1500
pen_origin = (0, 7)


##### Raspberry #####
rpi_ip = "10.3.141.1"
pwm_servo = 8
turn_on_led = 19
working_led = 21
button_pin = (16, 18)
bobines_motor1 = (29, 31, 33, 35)
bobines_motor2 = (7, 11, 13, 15)
