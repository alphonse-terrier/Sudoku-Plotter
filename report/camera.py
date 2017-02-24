#!/usr/bin/env python3


class Camera:
    """
    Permet la gestion de la camera de la raspberry pi
    Si celle-ci n'est pas disponible ou le module 'picamera'
    n'a pas été installé correctement, lève une exception.
    """

    def __init__(self, boss):
        self.boss = boss
        self.camera = None
        self.tryError()

    def tryError(self):
        try:
            import picamera
            self.camera = picamera.PiCamera()
        except:
            self.boss.setError("camera_error")

    def takePhoto(self):
        try:
            self.camera.capture("Images/photos.jpg")
            print("The photo has been taken")
        except:
            self.boss.setError("camera_error")

    
if __name__ == '__main__':
    class Boss:
        def setError(self, error):
            if error == "module_camera":
                print("Le module 'picamera' n'a pas été installé correctement !")
            if error == "disponibilite_camera":
                print("La caméra n'est pas disponible !")

    Camera = Camera(Boss())
    Camera.takePhoto()
