import time

import RPi.GPIO as GPIO

hall_sensor_A = 23
hall_sensor_B = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(hall_sensor_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(hall_sensor_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_A = True
previous_B = True

turn_count = 0


def handle_edge(hall_sensor):

    current_A = GPIO.input(hall_sensor_A)
    current_B = GPIO.input(hall_sensor_B)
    turn = 0
    
    global previous_A, previous_B, turn_count

    if hall_sensor == hall_sensor_A and current_A == 1:
        turn = 2 * previous_B - 1        

    if hall_sensor == hall_sensor_B and current_B == 1:
        turn = 1 - 2 * previous_A

    previous_A = current_A
    previous_B = current_B

    if turn == 0:
       return

    turn_count += turn

    print('turn: %d, count: %d' %(turn, turn_count) )


GPIO.add_event_detect(hall_sensor_A, GPIO.BOTH, handle_edge)
GPIO.add_event_detect(hall_sensor_B, GPIO.BOTH, handle_edge)
   

while True:
    time.sleep(1e6)
