import RPi.GPIO as IO
import PiMotor
import time


class LineSensingCyborgPi(object):
    def __init__(self):
        self.rightMotor = PiMotor.Motor("MOTOR2", 1)
        self.leftMotor = PiMotor.Motor("MOTOR1", 2)
        self.speed = 70  ##this is the universal speed setting used for manual control, which can be varied from 0 to 100
        self.baseSpeed = 50  ##this is the base speed into the motor used for PID

        self.stopSeconds(5)

        ##setting up the GPIOs for the IR sensors
        ##the numbering of the sensors aren't in sequence mainly due to which GPIO means are physically closest/convinient/neat
        ##to the sensors themselves
        self.LLSensor = 31  # 1st sensor from the left #no good 22 18 16 11 15 13 33 35 37 36
        self.LSensor = 38 # 2nd sensor from the left
        self.CSensor = 7  # sensor in the middle
        self.RSensor = 40  # 2nd sensor from the right
        self.RRSensor = 26  # 1st sensor from the right

        IO.setmode(IO.BOARD)

        IO.setup(self.LLSensor, IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(self.LSensor, IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(self.CSensor, IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(self.RSensor, IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(self.RRSensor, IO.IN, pull_up_down=IO.PUD_UP)

        ##Booleans that control the mode of the robot
        self.running = False
        self.linefollowing = False
        self.stopping = False
        self.exittingStop = False
        self.rotating = False

        ##Variables for PID

        self.kP = 8
        self.kI = 0
        self.kD = 3
        self.P = 0
        self.I = 0
        self.D = 0

        self.currentError = 0
        self.lastError = 0

    def pidForward(self):
        print "Left: ", self.baseSpeed + self.PID, " , right: ", self.baseSpeed - self.PID
        leftMotorInput = min(100, max(0,self.baseSpeed + self.PID))
        rightMotorInput = min(100, max(0,self.baseSpeed - self.PID))
        self.leftMotor.forward(leftMotorInput)
        self.rightMotor.forward(rightMotorInput)
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

    def readSensors(self):
        self.readings = 0b00000
        self.readings = self.readings + (IO.input(self.LLSensor) << 4)
        self.readings = self.readings + (IO.input(self.LSensor) << 3)
        self.readings = self.readings + (IO.input(self.CSensor) << 2)
        self.readings = self.readings + (IO.input(self.RSensor) << 1)
        self.readings = self.readings + (IO.input(self.RRSensor) << 0)

        ##Convert the raw readings to a error that we will use for the PID


    def setError(self):
        errorMap = {
            0b00001: 4,
            0b00011: 3,
            0b00010: 2,
            0b00110: 1,
            0b00100: 0,
            0b01100: -1,
            0b01000: -2,
            0b11000: -3,
            0b10000: -4,
            0b11110: 99,
            0b11101: 99,  # if four or more sensors returned true, we consider there to be a horizontal "stop" line
            0b11011: 99,
            0b10111: 99,
            0b01111: 99,
            0b11111: 99
        }
        self.lastError = self.currentError
        self.currentError = errorMap.get(self.readings, self.currentError)  ##if the reading is weird and not in the dictionary, we
        # default to last known error


    def calculatePID(self):
        self.P = self.currentError
        self.I = self.I + self.currentError
        self.D = self.currentError - self.lastError
        self.PID = self.kP * self.P + self.kI * self.I + self.kD * self.D


    def run(self):
        self.running = True
        self.runOperate()


    def linefollwing(self):
        self.readSensors()
        self.setError()
        self.calculatePID()

        if self.currentError == 99:
            self.linefollwing = False
            self.stopping = True
            return

        self.pidForward()
        ##otherwise, we are still in linefollowing mode:


    def stoppingState(self):
        self.stop()
        time.sleep(self.stopSeconds)
        self.stopping = False
        self.exittingStop = True


    def exittingStop(self):
        self.forward()
        time.sleep(0.2)
        self.exittingStop = False
        self.linefollwing = True

    def runOperate(self):
        self.linefollowing = True
        while (self.running):
            if self.linefollowing:
                self.linefollwing()
            if self.stopping:
                self.stoppingState()
            if self.exittingStop:
                pass
            if self.rotating:
                pass


pi = LineSensingCyborgPi()
pi.run()
