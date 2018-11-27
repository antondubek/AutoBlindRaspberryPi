
# Servo Control
import time
import wiringpi
import sys


def servocontroller(command):
    try:
        # arg1 = sys.argv[1] #Input
        #
        # print len(sys.argv)
        #
        # print arg1

        stop = 150
        clockwise = 50
        anticlockwise = 200

        # use 'GPIO naming'
        wiringpi.wiringPiSetupGpio()

        # set #18 to be a PWM output
        wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

        # set the PWM mode to milliseconds stype
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # divide down clock
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)

        delay_period = 0.01

        # while True:
        #         for pulse in range(50, 250, 1):
        #                 wiringpi.pwmWrite(18, pulse)
        #                 time.sleep(delay_period)
        #         for pulse in range(250, 50, -1):
        #                 wiringpi.pwmWrite(18, pulse)
        #                 time.sleep(delay_period)

        # while True:
        #     input = int(raw_input("Please insert a number: "))
        #     wiringpi.pwmWrite(18, input)

        print "Servo: Command received = " + command


        if command == 'open':
            print 'here'
            wiringpi.pwmWrite(18, clockwise)
            time.sleep(5)

        elif command == 'close':
            wiringpi.pwmWrite(18, anticlockwise)
            time.sleep(5)

        wiringpi.pwmWrite(18, 150)
        return

    except KeyboardInterrupt:
        print('Interrupted')
        wiringpi.pwmWrite(18, 150)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
