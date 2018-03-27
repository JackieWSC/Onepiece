import RPi.GPIO as gpio
import getopt
import sys
from time import sleep

def testing():
    gpio.setmode(gpio.BOARD)

    gpio.setup(11, gpio.OUT)
    gpio.setup(12, gpio.OUT)
    gpio.setup(16, gpio.OUT)
    gpio.setup(18, gpio.OUT)

    # move forward
    gpio.setup(11, gpio.LOW)
    gpio.setup(12, gpio.HIGH)
    gpio.setup(16, gpio.HIGH)
    gpio.setup(18, gpio.LOW)
    sleep(0.5)

    # move backward
    gpio.setup(11, gpio.HIGH)
    gpio.setup(12, gpio.LOW)
    gpio.setup(16, gpio.LOW)
    gpio.setup(18, gpio.HIGH)

    # move Left
    gpio.setup(11, gpio.LOW)
    gpio.setup(12, gpio.HIGH)
    gpio.setup(16, gpio.LOW)
    gpio.setup(18, gpio.HIGH)
    sleep(0.7)

    # move Left
    gpio.setup(11, gpio.HIGH)
    gpio.setup(12, gpio.LOW)
    gpio.setup(16, gpio.HIGH)
    gpio.setup(18, gpio.LOW)
    sleep(0.7)

    gpio.cleanup()


def init():
    gpio.setmode(gpio.BOARD)

    gpio.setup(11, gpio.OUT)
    gpio.setup(12, gpio.OUT)
    gpio.setup(16, gpio.OUT)
    gpio.setup(18, gpio.OUT)


def cleanup():
    gpio.cleanup()


def execute(left1, left2, right1, right2, time):
    gpio.output(11, left1)
    gpio.output(12, left2)
    gpio.output(16, right1)
    gpio.output(18, right2)
    sleep(time)
    stop()


def stop():
    gpio.output(11, gpio.LOW)
    gpio.output(12, gpio.LOW)
    gpio.output(16, gpio.LOW)
    gpio.output(18, gpio.LOW)


def forward():
    print 'Forward'
    execute(True, False, False, True, 0.5)


def backward():
    print 'Backward'
    execute(False, True, True, False, 0.5)


def left():
    print 'Left'
    execute(False, True, False, True, 0.2)


def right():
    print 'Right'
    execute(True, False, True, False, 0.2)


def run(command):
    print 'Command:', command

    optoins = {
        'w':forward,
        's':backward,
        'a':left,
        'd':right
    }

    for c in command:
        optoins[c]()


def Usage():
    print 'Command Car (v0.1) 24-Nov-2017'
    print 'manualMotorCar.py -c <command>'
    print 'e.g. manualMotorCar.py -c "wwawwdss"'


def main(argv):
    command = "wwawwdss"

    try:
        opts, args = getopt.getopt(argv, "hc:")
        if (len(opts) == 0):
            Usage()
            sys.exit(2)

    except getopt.GetoptError:
        Usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            Usage()
            sys.exit()
        elif opt in ("-c"):
            command = arg

    # run the command
    init()
    run(command)
    cleanup()


if __name__ == "__main__":
   main(sys.argv[1:])
