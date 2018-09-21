import smbus

channel = 1
address = 0x09

##initalize bus
bus = smbus.SMBus(channel)

readByte = 0L
while True:
    readByte = smbus.read_byte(channel)
    print readByte
