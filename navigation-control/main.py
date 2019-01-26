from time import sleep

from robot import Robot
from controller import PIDController
from manager import RoverManager

def main():
     dt = 1

     LEFT_MOTOR_INPUT = (17, 27)
     RIGHT_MOTOR_INPUT = (5, 6)
     
     LEFT_ENCODER_INPUT = {'hall_sensor_A': 23, 'hall_sensor_B': 24, 'ticks_per_revolution': 2400}
     RIGHT_ENCODER_INPUT = {'hall_sensor_A': 13, 'hall_sensor_B': 19, 'ticks_per_revolution': 2400}

     robot = Robot(LEFT_MOTOR_INPUT, RIGHT_MOTOR_INPUT, LEFT_ENCODER_INPUT, RIGHT_ENCODER_INPUT)
     controller = PIDController(robot)

     goal = {'x': 0 , 'y': 1}

     rover_manager = RoverManager(robot, controller)


     while(True):
        rover_manager.execute()
        sleep(dt)

if __name__ == '__main__':
    main()