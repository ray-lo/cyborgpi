import RPi.GPIO as IO
#IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(2,IO.IN)

while (True):
    print IO.input(2)