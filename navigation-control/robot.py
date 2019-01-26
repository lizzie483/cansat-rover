import math

from gpiozero import Motor

from encoder import QuadratureEncoder

class Robot():
    def __init__(self, left_motor_input, right_motor_input, left_encoder_input, right_encoder_input):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.wheel_radius = 0.139
        self.wheel_base_length = 0.212
        self.left_wheel_speed = 0
        self.right_wheel_speed = 0
        self.left_motor = Motor(left_motor_input[0], left_motor_input[1])
        self.right_motor = Motor(right_motor_input[0], right_motor_input[1])
        self.left_encoder = QuadratureEncoder(left_encoder_input['ticks_per_revolution'], left_encoder_input['hall_sensor_A'], left_encoder_input['hall_sensor_B'])
        self.right_encoder = QuadratureEncoder(right_encoder_input['ticks_per_revolution'], right_encoder_input['hall_sensor_A'], right_encoder_input['hall_sensor_B'])

    def forward(self, speed = 1):
        self.left_motor.forward(speed)
        self.right_motor.forward(speed)

    def backward(self, speed = 1):
        self.left_motor.backward(speed)
        self.right_motor.backward(speed)

    def update_speed(self, left_speed, right_speed):
        pass

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()