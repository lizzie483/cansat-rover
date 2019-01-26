import math
import RPi.GPIO as GPIO

class QuadratureEncoder():
    def __init__(self, ticks_per_revolution, hall_sensor_A, hall_sensor_B):
        self.L = 0.212
        self.R = 0.139
        self.counter = 0
        self.ticks_per_revolution = ticks_per_revolution
        self.hall_sensor_A = hall_sensor_A
        self.hall_sensor_B = hall_sensor_B
        self.previous_A = True
        self.previous_B = True

        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        #print("A: %d, B: %d" %(self.hall_sensor_A, self.hall_sensor_B))
        GPIO.setup(self.hall_sensor_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.hall_sensor_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.hall_sensor_A, GPIO.BOTH, self.handle_edge)
        GPIO.add_event_detect(self.hall_sensor_B, GPIO.BOTH, self.handle_edge)

    def diatance_per_ticks(self, ticks):
        return 2 * math.pi * self.R / self.ticks_per_revolution * ticks


    def handle_edge(self, hall_sensor):
        current_A = GPIO.input(self.hall_sensor_A)
        current_B = GPIO.input(self.hall_sensor_B)

        turn = 0

        if hall_sensor == self.hall_sensor_A and current_A == 1:
            turn = 2 * self.previous_B - 1

        if hall_sensor == self.hall_sensor_B and current_B == 1:
            turn = 1 - 2 * self.previous_A

        self.previous_A = current_A
        self.previous_B = current_B

        #print("turn: %d" %turn)
        self.counter += turn
        #print("counter: %d"  %self.counter)
