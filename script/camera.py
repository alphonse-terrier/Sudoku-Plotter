#!/usr/bin/env python3

from PIL import Image
import numpy as np
from time import *


class Camera:
    """
    Permet la gestion de la camera de la raspberry pi
    Si celle-ci n'est pas disponible ou le module 'picamera'
    n'a pas été installé correctement, lève une exception.
    """

    def __init__(self, boss):
        self.boss = boss
        self.camera = None
        self.image = None
        self.pixel = None
        self.size = (0, 0)
        self.tryError()

    def tryError(self):
        try:
            import picamera
            self.camera = picamera.PiCamera()
        except:
            self.boss.setError("camera_error")

    def takePhoto(self):
        try:
            self.camera.capture("../pictures/sudoku.jpg")
            print("The photo has been taken")
        except:
            self.boss.setError("camera_error")

    def sendPhoto(self):
        zero = time()
        text = ""
        self.image = Image.open("../pictures/Sudoku.jpg").convert("L")
        self.size = self.image.size
        self.pixel = np.asarray(self.image)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                text += str(self.pixel[j, i]) + ' '


if __name__ == '__main__':
    class Boss:
        def setError(self, error):
            if error == "module_camera":
                print("Le module 'picamera' n'a pas été installé correctement !")
            if error == "disponibilite_camera":
                print("La caméra n'est pas disponible !")

    Camera(Boss()).sendPhoto()
    # Camera.takePhoto()
