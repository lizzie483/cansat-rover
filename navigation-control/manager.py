import math

class RoverManager():
    def __init__(self, robot, controller, goal):
        self.robot = robot
        self.controller = controller
        self.previous_left_ticks = 0
        self.previous_right_ticks = 0
        self.goal = goal

    
    def distance_per_ticks(self, ticks, wheel_radius, ticks_per_revolution):
        return 2 * math.pi * wheel_radius / ticks_per_revolution * ticks

    def update_odometry(self):

        left_encoder_ticks = self.robot.left_encoder.counter
        right_encoder_ticks = self.robot.right_encoder.counter
        left_wheel_distance = self.distance_per_ticks(left_encoder_ticks - self.previous_left_ticks, self.robot.wheel_radius, self.robot.left_encoder.ticks_per_revolution)
        right_wheel_distance = self.distance_per_ticks(right_encoder_ticks - self.previous_right_ticks, self.robot.wheel_radius, self.robot.right_encoder.ticks_per_revolution)

        distance = (left_wheel_distance + right_wheel_distance ) / 2
        phi = (right_wheel_distance - left_wheel_distance) / self.robot.wheel_base_length

        dx = distance * math.cos(self.robot.theta)
        dy = distance * math.sin(self.robot.theta)
        dtheta = phi

        self.robot.x += dx
        self.robot.y += dy
        self.robot.theta += dtheta

        self.previous_left_ticks = left_encoder_ticks
        self.previous_right_ticks = right_encoder_ticks

    def unicycle_to_differential(self, v, w):
        left_speed = (2 * v + w * self.robot.wheel_base_length) / (2 * self.robot.wheel_radius)
        right_speed = (2 * v - w * self.robot.wheel_base_length) / (2 * self.robot.wheel_radius)

        return left_speed, right_speed

    def execute(self):
        v, w = self.controller.control(self.goal)

        left_speed, right_speed = self.unicycle_to_differential(v, w)
        self.robot.left_speed = left_speed
        self.robot.right_speed = right_speed

        self.update_odometry()