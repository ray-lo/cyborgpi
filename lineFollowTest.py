import smbus

channel = 1
address = 0x09

##initalize bus
bus = smbus.SMBus(channel)

readByte = 0L
while True:
    readByte = bus.read_byte(address,16)
    print readByte
