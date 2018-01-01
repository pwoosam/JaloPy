from Adafruit_PCA9685 import PCA9685
import time
import getch

pwm = PCA9685()

motor_min = 1700
motor_max = 2500
servo_min = 1500
servo_max = 2700

def pulse_from_to(channel, start, end):
    pwm.set_pwm(channel, 0, start)
    if start > end:
        [pwm.set_pwm(channel, 0, i) for i in reversed(range(end, start + 1))]
    else:
        [pwm.set_pwm(channel, 0, i) for i in range(start, end + 1)]


pwm.set_pwm_freq(300)
motor_pulse = 2150
servo_pulse = 2250

steer_speed = 100
motor_speed = 2
direction = 'forward'

seq = 0
count = 0

try:
    while True:
        char = getch.getch()
        if char == '\x1b' and seq == 0:
            seq += 1
            continue
        elif char == '[' and seq == 1:
            seq += 1
            continue
        elif seq == 2:
            if char == 'A':
                char = 'up'
            elif char == 'B':
                char = 'down'
            elif char == 'C':
                char = 'right'
            elif char == 'D':
                char = 'left'
            seq = 0
        else:
            seq = 0


        if char == 'up' and motor_pulse < motor_max:
            # forward at 2200
            if motor_pulse > 2124 and direction != 'forward':
                pulse_from_to(1, 2400, 2150)
                pulse_from_to(1, 2150, 2204)
                motor_pulse = 2204
                direction = 'forward'
            elif motor_pulse < 2124:
                motor_pulse += motor_speed
            elif motor_pulse < 2204 and direction == 'forward':
                motor_pulse = 2204
            else:
                motor_pulse += motor_speed
        elif char == 'down' and motor_pulse > motor_min:
            # reverse at 2124
            if motor_pulse < 2124 and direction != 'reverse':
                pulse_from_to(1, 1900, 2150)
                pulse_from_to(1, 2150, 2124)
                motor_pulse = 2124
                direction = 'reverse'
            elif motor_pulse > 2124 and motor_pulse < 2204:
                motor_pulse = 2124
            else:
                motor_pulse -= motor_speed
        elif char == 'right' and servo_pulse > servo_min:
            servo_pulse -= steer_speed
        elif char == 'left' and servo_pulse < servo_max:
            servo_pulse += steer_speed
        elif char == 'd':
            servo_pulse = servo_min
        elif char == 'a':
            servo_pulse = servo_max
        elif char == 's':
            servo_pulse = 2250
        elif char == ' ':
            pulse_from_to(1, motor_pulse, 2150)
            motor_pulse = 2150
        elif char == 'r':
            motor_pulse = motor_min
        elif char == 'f':
            motor_pulse = motor_max
        print('motor_pulse = {}\nservo_pulse = {}\n{}'.format(motor_pulse, servo_pulse, char))

        pwm.set_pwm(0, 0, servo_pulse)
        pwm.set_pwm(1, 0, motor_pulse)
except KeyboardInterrupt:
    pwm.set_pwm(0, 0, 0)
    pwm.set_pwm(1, 0, 0)

#pulse_from_to(1, motor_min, motor_max)
#pulse_from_to(1, motor_max, 0)
#pulse_from_to(1, 0, motor_min)
#print('at neutral')
