# cyborgpi

**09/20/2018**: It turns out the Pi will apepar to be on if the battery is low. SSH connection gets quite bad when the battery is low. If there is connectivity issues, change/charge batteries first.

Currently debugging issues regardig why the car wont' track straight.

**11/01/2018**: Having realized that the motors simply don't have enough fidelity to track straight at lower speeds (or even at full speed, for that matter), we need some sort of feedback system. The simplest solution is a line sensing device. By placing an array (two minimum) of Infared sensors, that changes its reading when it detects a change from say a white floor to a black floor, we can have a robot that follows black tape on the floor. 

The Sunfounder 8 sensor line follower module communicates through I2C, which could have been ideal, except it keeps getting dropped after one I2C bus detect ("sudo i2cdetect -y 1" in the terminal). As in, the device would show up correctly after one i2cdetect call, but dissapears after subsequent calls. Python code doesn't exist for the 8-sensor version, but does for the 5-sensor version. I have tried modifying the 5-sensor version to no avail. It's possible it's because the device wants 5v, while the Pi's GPIO pins operate at 3.3v.

I asked Deb to buy 5 SparkFun QRE1113 (digital) sensors for me. They are advertised to work on 3.3v so should have been just plug-into-GPIO-pins-on-the-Pi-and-play sort of deal. Unfortunately, it is not so right now. Plugging it in into any of the GPIO pins seem to have no bearing on the actual signal read (it's either always "1" or always "0" depending on the pin used). I have eliminated the possibility of the Sunfounder motor shield (used to control the motors for the wheels) by removing the shield and testing out the IR sensor directly. Next move is to try a different Pi. I also posted it as a question on the RaspPi forum. Hopefully some DIY genius can help us out. 
  https://www.raspberrypi.org/forums/viewtopic.php?f=37&t=225960&sid=bfba82c972c4f15f31b83be62f50bac6
  
