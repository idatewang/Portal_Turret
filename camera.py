#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import RPi.GPIO as GPIO

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.x_og = 0
        self.y_og = 0

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self,servo1,servo_pos):
        frame = self.flip_if_needed(self.vs.read())
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        if(len(faces)>0):
            print("Detected.")
            for (x, y, w, h) in faces:
                if self.x_og == 0 and self.y_og == 0:
                    self.x_og = x
                    self.y_og = y
                if servo_pos != servo_pos+0.05266*(x-self.x_og) and (x-self.x_og<10) and (x-self.x_og>-10):                    
                    servo_pos = servo_pos+0.05266*(x-self.x_og)
                    servo1.ChangeDutyCycle(servo_pos)
                    time.sleep(1)
                    print(servo_pos)
                    print("Change in x:",str(x-self.x_og))
                    print("Change in y:",str(y-self.y_og))
                self.x_og = x
                self.y_og = y
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', np.flip(frame, 0))        
        return jpeg.tobytes()

    def get_frame_test(self):
        frame = self.flip_if_needed(self.vs.read())
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame
