import RPi.GPIO as IO
import PiMotor
import time
import sys

class LineSensingCyborgPi(object):
    def __init__(self):
        self.rightMotor = PiMotor.Motor("MOTOR2", 1)
        self.leftMotor = PiMotor.Motor("MOTOR1", 2)
        self.speed = 70   ##this is the universal speed setting used for manual control, which can be varied from 0 to 100
        self.baseSpeed = 50  ##this is the base speed into the motor used for PID
        self.rotateSpeed = 40
        self.stopSeconds = 20

        ##setting up the GPIOs for the IR sensors
        ##the numbering of the sensors aren't in sequence mainly due to which GPIO means are physically closest/convinient/neat
        ##to the sensors themselves
        self.LLSensor = 29  # 1st sensor from the left #no good 11 13 15 16 18 22 33 35 36 37 
        self.LSensor = 38 # 2nd sensor from the left
        self.CSensor = 19  # sensor in the middle
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

        self.kP = 25
        self.kI = 0
        self.kD = 15
        self.P = 0
        self.I = 0
        self.D = 0

        self.currentError = 0
        self.lastError = 0
    
    def forwardAndReverse(self, leftMotorInput, rightMotorInput):
        if leftMotorInput >= 0:
            self.leftMotor.forward(leftMotorInput)
        else:
            self.leftMotor.reverse((-1)* leftMotorInput)
        if rightMotorInput >=0:
            self.rightMotor.forward(rightMotorInput)
        else:
            self.rightMotor.reverse((-1)*rightMotorInput)
    
    def pidForward(self):
        print "Left: ", self.baseSpeed + self.PID, " , right: ", self.baseSpeed - self.PID
        leftMotorInput = min(100, max(-100,self.baseSpeed + self.PID))
        rightMotorInput = min(100, max(-100, self.baseSpeed - self.PID))
        self.forwardAndReverse(leftMotorInput, rightMotorInput)

    def forward(self):
        self.leftMotor.forward(self.speed)
        self.rightMotor.forward(self.speed)


    def reverse(self):
        self.leftMotor.reverse(self.speed)
        self.rightMotor.reverse(self.speed)


    def rotateLeft(self):
        self.leftMotor.reverse(self.rotateSpeed)
        self.rightMotor.forward(self.rotateSpeed)


    def rotateRight(self):
        self.leftMotor.forward(self.rotateSpeed)
        self.rightMotor.reverse(self.rotateSpeed)


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
            0b00001: 16,
            0b00011: 9,
            0b00010: 4,
            0b00110: 1,
            0b00100: 0,
            0b01100: -1,
            0b01000: -4,
            0b11000: -9,
            0b10000: -16,
            0b11111: 99, ##stop on solid line
            0b00000: -99 ##rotate when there is no line
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


    def linefollwingState(self):
        self.readSensors()
        self.setError()
        self.calculatePID()
        print (format(self.readings, '05b'))
        if self.currentError == 99:
            print("99 detected")
            self.linefollwing = False
            self.stopping = True
            return
        if self.currentError == -99:
            self.linefollowing = False
            self.rotating = True
            return
        self.pidForward()
        ##otherwise, we are still in linefollowing mode:


    def stoppingState(self):
        self.stop()
        time.sleep(self.stopSeconds)
        self.stopping = False
        self.exittingStop = True


    def exittingStopState(self):
        self.forward()
        time.sleep(0.2)
        self.exittingStop = False
        self.linefollwing = True
    
    def rotatingState(self):
        self.readSensors()
        self.setError()
        if (self.currentError != -99):
            self.rotating = False
            self.linefollowing = True
            return
        self.rotateLeft()

    def runOperate(self):
        try:
            self.linefollowing = True
            while (self.running):
                if self.linefollowing:
                    self.linefollwingState()
                if self.stopping:
                    self.stoppingState()
                if self.exittingStop:
                    self.exittingStopState()
                if self.rotating:
                    self.rotatingState()
        except KeyboardInterrupt:
            print "Stopping robot"
            self.stop()
            sys.exit(0)


pi = LineSensingCyborgPi()
pi.run()
