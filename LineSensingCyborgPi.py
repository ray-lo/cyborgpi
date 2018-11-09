import RPi.GPIO as IO

##the numbering of the sensors aren't in sequence mainly due to which GPIO means are physically closest/convinient/neat to the sensors themselves
LLSensor = 24 #1st sensor from the left
LSensor = 20 #2nd sensor from the left
CSensor = 23 #sensor in the middle
RSensor = 21 #2nd sensor from the right
RRSensor = 7 #1st sensor from the right


IO.setmode (IO.BCM)
IO.setup(LLSensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(LSensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(CSensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(RSensor, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(RRSensor, IO.IN, pull_up_down=IO.PUD_UP)

inputs = [0,0,0,0,0]
while (True):
	inputs[0] = IO.input(LLSensor)
	inputs[1] = IO.input(LSensor)
	inputs[2] = IO.input(CSensor)
	inputs[3] = IO.input(RSensor)
	inputs[4] = IO.input(RRSensor)
	print inputs
