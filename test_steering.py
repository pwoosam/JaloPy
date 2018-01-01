from Adafruit_PCA9685 import PCA9685
import time

pwm = PCA9685()

servo_min = 250
servo_max = 450

pulse = servo_min
increasing = True
step_size = 1
while True:
    pwm.set_pwm(0, 0, pulse)
    if pulse < servo_max and increasing:
        pulse += step_size
        increasing = True
    elif pulse > servo_min:
        pulse -= step_size
        increasing = False
    else:
        pulse += step_size
        increasing = True
    time.sleep(0.01)
    print(pulse)

while False:
    pwm.set_pwm(0, 0, servo_min)
    time.sleep(0.5)
    pwm.set_pwm(0, 0, servo_max)
    time.sleep(0.5)

pwm.set_pwm(0, 0, 0)
