import math

class PIDController():
    def __init__(self, robot):
        self.robot = robot
        self.speed = 0.556
        self.kp = 2
        self.ki = 0
        self.kd = 0
        self.previous_error = 0
        self.integral_error = 0

    def control(self, target):

        u_x = target['x'] - self.robot.x
        u_y = target['y'] - self.robot.y

        print('ux: %f, uy: %f' %(u_x, u_y))

        target_theta = math.atan2(u_y, u_x)

        u_theta = target_theta - self.robot.theta

        print('g_theta: %f, u_theta: %f' %(target_theta, u_theta))

        current_error = math.atan2(math.sin(u_theta), math.cos(u_theta))

        differential_error = current_error - self.previous_error
        integral_error = current_error + self.integral_error

        self.previous_error = current_error
        self.integral_error = integral_error

        w = current_error * self.kp + differential_error * self.kd + integral_error * self.ki

        print('w: %f' %w)

        return self.speed, w
