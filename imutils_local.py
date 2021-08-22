#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os

import cv2

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

while True:
    frame = pi_camera.get_frame_test()
    cv2.imshow("s",frame)    
    key = cv2.waitKey(1) & 0xFF
         
        # Clear the stream in preparation for the next frame
    if key == ord("q"):
        break


