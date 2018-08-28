import PiMotor
import time
import pygame

class RemoteCyborgPi(object):

    def __init__(self):
        self.leftMotor = PiMotor.motor("MOTOR1", 1)
        self.rightMotor = PiMotor.motor("MOTOR2", 2)

    def forward(self):
        self.leftMotor.forward(100)
        self.rightMotor.forward(100)

    def rotateleft(self):
        self.leftMotor.reverse(100)
        self.rightMotor.forward(100)

    def rotateRight(self):
        self.leftMotor.forward(100)
        self.rightMotor.reverse(100)

    def left(self):
        self.leftMotor.stop()
        self.rightMotor.forward(100)

    def right(self):
        self.leftMotor.forward(100)
        self.rightMotor.stop()

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()




myPi = RemoteCyborgPi.__init__()
while 1:
    myPi.left()
    time.sleep(1000)
    myPi.right()
    time.sleep(1000)
    myPi.forward()
    time.sleep(1000)
    myPi.reverse()
    time.sleep(1000)
    myPi.stop()

