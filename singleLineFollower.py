import RPi.GPIO as IO
#IO.setwarnings(False)
sensor = 25
IO.setmode (IO.BCM)
IO.setup(sensor, IO.IN, pull_up_down=IO.PUD_UP)
while (True):
   # if IO.input(sensor) != 0:
	#print "Hit"
    print IO.input(sensor)
