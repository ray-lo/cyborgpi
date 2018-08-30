import PiMotor
import time
import curses

class RemoteCyborgPi(object):

    def __init__(self):
        self.rightMotor = PiMotor.Motor("MOTOR1", 1)
        self.leftMotor = PiMotor.Motor("MOTOR2", 1)


    def forward(self):
        self.leftMotor.forward(100)
        self.rightMotor.forward(100)
    def reverse(self):
        self.leftMotor.reverse(100)
        self.rightMotor.reverse(100)

    def rotateLeft(self):
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
        if key == "UP":
            myPi.forward()
        if key == "DOWN":
            myPi.reverse()
        else:
            myPi.stop()


        #screen.addstr(0, 0, 'key: {:<10}'.format(key))



curses.wrapper(main)



