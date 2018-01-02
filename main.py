import pygame
import time
import os
import sys
from motor_controller import MotorController
from controller import Joystick

if __name__ == '__main__':
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.joystick.init()

    motoCon = MotorController()
    # if controllerJoystickIsUp:
    #   motoCon.forward()
    with Joystick(0) as controller:
        while True:
            controller.update()
            inputs = controller.get_all_vals()
            if inputs['button_0']:
                motoCon.forward()
            elif inputs['button_1']:
                motoCon.stop()
            elif inputs['button_2']:
                motoCon.reverse()
            motoCon.set_steering(inputs['axis_0'])
            motoCon.print_stat()
            time.sleep(0.1)
            
