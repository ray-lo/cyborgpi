import RPi.GPIO as IO

##the numbering of the sensors aren't in sequence mainly due to which GPIO means are physically closest/convinient/neat to the sensors themselves
LLSensor = 24 #1st sensor from the left
LSensor = 21 #2nd sensor from the left
CSensr = 23 #sensor in the middle
RSensor = 20 #2nd sensor from the right
RRSensor = 26 #1st sensor from the right


IO.setmode (IO.BCM)
IO.setup(LLsensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(Lsensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(Csensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(Rsensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(RRsensor, IO.IN, pull_up_down=IO.PUD_UP)

while (True):
   # if IO.input(sensor) != 0:
	#print "Hit"
    print IO.input(sensor)
