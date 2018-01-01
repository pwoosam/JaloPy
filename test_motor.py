from Adafruit_PCA9685 import PCA9685
import time

pwm = PCA9685()

motor_min = 350
motor_max = 450

pulse = servo_min
increasing = True
step_size = 1
while False:
    pwm.set_pwm(1, 0, pulse)
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
    pwm.set_pwm(1, 0, servo_min)
    time.sleep(0.5)
    pwm.set_pwm(1, 0, servo_max)
    time.sleep(0.5)

def pulse_from_to(channel, start, end):
    def delay_set_pwm(pulse):
        time.sleep(0.1)
        pwm.set_pwm(channel, 0, pulse)
        print(pulse)
    pwm.set_pwm(channel, 0, start)
    input('Waiting at {}'.format(start))
    if start > end:
        [delay_set_pwm(i) for i in reversed(range(end, start + 1))]
    else:
        [delay_set_pwm(i) for i in range(start, end + 1)]
    print('at {}'.format(end))

pwm.set_pwm_freq(50)
pulse_from_to(1, motor_min, motor_max)
pulse_from_to(1, motor_max, 0)
pulse_from_to(1, 0, motor_min)
print('at neutral')
