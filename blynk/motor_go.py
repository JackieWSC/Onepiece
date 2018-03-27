import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)

gpio.setup(11, gpio.OUT)
gpio.setup(12, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(38, gpio.OUT)
gpio.setup(40, gpio.OUT)


gpio.output(11, gpio.LOW)
gpio.output(12, gpio.HIGH)
gpio.output(16, gpio.LOW)
gpio.output(18, gpio.HIGH)
l = gpio.PWM(38, 20)
r = gpio.PWM(40, 20)
l.start(40)
r.start(40)

time.sleep(2)

l.stop()
r.stop()

gpio.cleanup()
