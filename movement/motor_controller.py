#!/usr/bin/env python3
from Adafruit_PCA9685 import PCA9685
import time

class MotorController:
    def __init__(self):
        self.pwm = PCA9685()

        # Set the frequency high for motors to run smoothly
        # We need to change this to preserve the servo later...
        self.pwm.set_pwm_freq(300)

        # Based on the pwm frequency, these variables represent
        # max and min speeds/directions
        self.motor_min = 1700
        self.motor_max = 2500
        self.servo_min = 1800
        self.servo_max = 2700 

        # Set the initial neutral speed/direction
        self.motor_pulse = 2150
        self.servo_pulse = 2250

        # Configure how quickly values change
        self.motor_speed = 2

        # Keep track of the current motor direction
        self.direction = 'forward'

    def pulse_from_to(self, channel, start, end):
        self.pwm.set_pwm(channel, 0, start)
        if start > end:
            [self.pwm.set_pwm(channel, 0, i) for i in reversed(range(end, start +1))]
        else:
            [self.pwm.set_pwm(channel, 0, i) for i in range(start, end+1)]
    
    def forward(self):
        if self.motor_pulse <= self.motor_max:
            #foward at 2200
            if self.motor_pulse > 2124 and self.direction != 'forward':
                self.set_forward()
                self.motor_pulse = 2204
            elif self.motor_pulse < 2124:
                self.motor_pulse += self.motor_speed
            elif self.motor_pulse < 2204 and self.direction == 'forward':
                self.motor_pulse = 2204
            else:
                self.motor_pulse += self.motor_speed
            self.pwm.set_pwm(1, 0, self.motor_pulse)
       
    def reverse(self):
        #reverse at 2124
        if self.motor_pulse >= self.motor_min:
            if self.motor_pulse < 2124 and self.direction != 'reverse':
                self.set_reverse()
                self.motor_pulse = 2124
            elif self.motor_pulse > 2124 and self.motor_pulse < 2204:
                self.motor_pulse = 2124
            else:
                self.motor_pulse -= self.motor_speed
            self.pwm.set_pwm(1, 0, self.motor_pulse)

    def stop(self):
        self.pulse_from_to(1, self.motor_pulse, 2150)
        self.motor_pulse = 2150
        self.pwm.set_pwm(1, 0, self.motor_pulse)
            
    def print_stat(self):
        print('self.motor_pulse = {}\tself.servo_pulse = {}'.format(self.motor_pulse, self.servo_pulse))

    def set_forward(self):
        self.pulse_from_to(1, 2400, 2150)
        self.pulse_from_to(1, 2150, 2204)
        self.direction = 'forward'

    def set_reverse(self):
        self.pulse_from_to(1,1900,2150)
        self.pulse_from_to(1, 2150, 2124)
        self.direction = 'reverse'
    
    def set_steering(self, value):
        new_val = value * -450 + 2250
        self.pwm.set_pwm(0, 0, int(new_val))
