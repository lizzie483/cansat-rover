import cv2  # Importamos libreria OpenCV 3.4
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray




class ImageProcessing():
    def __init__(self,robot, height_resolution, width_resolution):
        self.direction = 0
        self.searching = 0
        self.movement = 0
        self.kernel_open = np.np.ones((5, 5))
        self.kernel_closure = np.ones((20, 20))
        self.upper_bound = np.array([102, 255, 255])
        self.lower_bound = np.array([33, 80, 40])
        self.height = height_resolution
        self.width = width_resolution
        self.camera = PiCamera()
        self.camera.resolution = (width_resolution, height_resolution)
        self.camera.framerate = 32
        self.raw_capture = PiRGBArray(self.camera,size= (self.width,self.width))
        self.robot = robot

    def execute(self):

        for self.frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            self.image = self.frame.array
            cv2.imshow("Frame", self.image)
            key = cv2.waitKey(1) & 0xFF

            #RGB to HSV
            imgHSV = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

            #Color Range
            mask = cv2.inRange(imgHSV, self.lower_bound, self.upper_bound)

            #Morphology
            mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel_open)
            mask_closure = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, self.kernel_closure)
            mask_final = mask_closure

            _, conts, h = cv2.findContours(mask_final.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            cv2.line(self.image, (int(7 * self.width / 16), 0), (int(7 * self.width / 16), self.height), (80, 100, 80), 3)
            cv2.line(self.image, (int(9 * self.width / 16), 0), (int(9 * self.width / 16), self.height), (80, 100, 80), 3)

            if bool(conts):


                self.searching = 1

                mcont = max(conts, key=cv2.contourArea)
                cv2.drawContours(self.image, mcont, -1, (255, 0, 0), 3)
                x, y, w, h = cv2.boundingRect(mcont)
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                lineThickness = 2
                average_width = int(x + w / 2)
                cv2.line(self.image, (average_width, y), (average_width, y + h), (0, 255, 0), 2)

                half_width = self.width / 2
                width_difference = average_width - half_width
                speed_rate = abs(width_difference)

                # Navigation
                if (average_width > 7 * self.width / 16 and average_width < 9 * self.width / 16):
                    self.movement = 1

                elif (average_width > 9 * self.width / 16):
                    self.movement = 2

                else:
                    self.movement = 3

                if (h >= 0.6 * self.height):
                    self.movement = 4


            self.rawCapture.truncate(0)

            if bool(self.searching):

                if (self.movement == 1):
                    print("Straight")
                    self.robot.update_speed(0.45,0.45)

                if (self.movement == 2):
                    print("Right")
                    speed_final = 0.35 + ((speed_rate/half_width)/100)
                    self.robot.update_speed(speed_final,0.35)

                if (self.movement == 3):
                    print("Left")
                    speed_final = 0.35 + ((speed_rate / half_width) / 100)
                    self.robot.update_speed(0.35,speed_final)

                if (self.movement == 4):
                    print("Stop")
                    self.robot.stop()
                    break

            else:
                print("Searching")
