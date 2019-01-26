import math
from time import sleep

from gpiozero import Motor

from encoder import QuadratureEncoder

class Robot():
    def __init__(self, left_motor_input, right_motor_input):
        self.x = 0
        self.y = 0
        self.w = 0
        self.left_motor = Motor(left_motor_input[0], left_motor_input[1])
        self.right_motor = Motor(right_motor_input[0], right_motor_input[1])

    def forward(self, speed = 1):
        self.left_motor.forward(speed)
        self.right_motor.forward(speed)

    def backward(self, speed = 1):
        self.left_motor.backward(speed)
        self.right_motor.backward(speed)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def update_position(dx, dy, dw):
        self.x += dx
        self.y += dy
        self.w += dw

    def moveTo(x, y):
        dx = x - self.x
        dy = y - self.y

        w = atan2(dy, dx)

   def control(w):
        error = w
        d_error = error - previous_w
        i_error += error

        return kp * error + kd * d_error + ki * i_error        
    

def main():
     dt = 1

     LEFT_MOTOR_INPUT = (17, 27)
     RIGHT_MOTOR_INPUT = (5, 6)
     
     LEFT_ENCODER_INPUT = (23, 24)
     RIGHT_ENCODER_INPUT = (13, 19)

     robot = Robot(LEFT_MOTOR_INPUT, RIGHT_MOTOR_INPUT)
     left_encoder = QuadratureEncoder(LEFT_ENCODER_INPUT[0], LEFT_ENCODER_INPUT[1])
     right_encoder = QuadratureEncoder(RIGHT_ENCODER_INPUT[0], RIGHT_ENCODER_INPUT[1])

     robot.forward()

     while(True):
         print(left_encoder.counter)
         print(right_encoder.counter)
         sleep(dt)

if __name__ == '__main__':
    main()



