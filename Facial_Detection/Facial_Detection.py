from .gaze_tracking import GazeTracking
import cv2
import os
import sys

if getattr(sys, 'frozen', False):
    folder_path = os.path.dirname(sys.executable)
else:
    folder_path = os.path.dirname(__file__)

gaze = GazeTracking(folder_path)

path2file = os.path.join(folder_path, "trained_models/haarcascade_frontalface_default.xml")
cascade_face = cv2.CascadeClassifier(path2file)


class Facial_Monitor():
    def __init__(self, image):
        self.image=image
        self.eyewarning=1
        self.facewarning=1

    def eyegaze_detection(self):
        gaze.refresh(self.image)
        self.image = gaze.annotated_frame()
        if gaze.is_right() or gaze.is_left():
            self.eyewarning=0
        else:
            self.image=None

    def face_detection(self):
        grayscale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        face = cascade_face.detectMultiScale(grayscale, scaleFactor = 1.25,
                                                        minNeighbors = 5)
        if len(face) == 0:
            self.facewarning=0
        elif len(face) >= 2:
            self.facewarning = 2
        else:
            self.image = None
