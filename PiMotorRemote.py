
import PiMotor
import time
import curses

class RemoteCyborgPi(object):

    def __init__(self):
        self.rightMotor = PiMotor.Motor("MOTOR2", 1)
        self.leftMotor = PiMotor.Motor("MOTOR1", 2)
	self.speed = 100

    def forward(self):
        self.leftMotor.forward(self.speed)
        self.rightMotor.forward(self.speed)
    def reverse(self):
        self.leftMotor.reverse(self.speed)
        self.rightMotor.reverse(self.speed)

    def rotateLeft(self):
        self.leftMotor.reverse(self.speed)
        self.rightMotor.forward(self.speed)

    def rotateRight(self):
        self.leftMotor.forward(self.speed)
        self.rightMotor.reverse(self.speed)

    def left(self):
        self.leftMotor.stop()
        self.rightMotor.forward(self.speed)

    def right(self):
        self.leftMotor.forward(self.speed)
        self.rightMotor.stop()

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()


def testRun():
    while 1:
        myPi.left()
        time.sleep(2)
        myPi.right()
        time.sleep(2)
        myPi.rotateLeft()
        time.sleep(2)
        myPi.rotateRight()
        time.sleep(2)
        myPi.forward()
        time.sleep(2)
        myPi.reverse()
        time.sleep(2)
        myPi.stop()

def main(screen):
    myPi = RemoteCyborgPi()

    key = ''
    while key != 'q':
        key = screen.getkey()
        if key == "KEY_UP":
            myPi.forward()
        elif key == "KEY_DOWN":
            myPi.reverse()

        elif key == "KEY_LEFT":
            myPi.left()
        elif key == "KEY_RIGHT":
            myPi.right()
        elif key == "z":
            myPi.rotateLeft()
        elif key == "x":
            myPi.rotateRight()
        else:
            myPi.stop()


        #screen.addstr(0, 0, 'key: {:<10}'.format(key))



curses.wrapper(main)



