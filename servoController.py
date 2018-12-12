
# Servo Control
import time
import wiringpi
import sys

currentPosition = 0
pwmPin = 18
timeToMovePosition = 2

stop = 150
clockwise = 50
anticlockwise = 200


# Simple getter for the current position
def getCurrentPosition():
    return str(currentPosition)

# Checks the current position and how far the servo must move to get to the position passed
# Then engages the motor in the correct direction so it gets there.
def moveServo(positionToMove):
    global currentPosition

    #If we arent currently in the position passed
    if currentPosition != positionToMove:
        print 'Blind moving from position %s to %s' %(str(currentPosition), str(positionToMove))

        #Calculate distance we need to move
        amountToMove = currentPosition - positionToMove

        #Check if need to go up or down and get motor moving
        if amountToMove > 0: #Means we are going down
            wiringpi.pwmWrite(pwmPin, clockwise)
        else: #means we are going up
            wiringpi.pwmWrite(pwmPin, anticlockwise)

        #Sleep for the amount of time to get to the position
        timeToSleep = abs(amountToMove) * timeToMovePosition
        time.sleep(timeToSleep)

        #Stop the motor
        wiringpi.pwmWrite(pwmPin, stop)
    else:
        print 'Blind already in that position'

    # Set the position
    currentPosition = positionToMove
    return


def servocontroller(command):
    try:
        # use 'GPIO naming'
        wiringpi.wiringPiSetupGpio()

        # set pin to be a PWM output
        wiringpi.pinMode(pwmPin, wiringpi.GPIO.PWM_OUTPUT)

        # set the PWM mode to milliseconds
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # divide down clock
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)

        delay_period = 0.01

        #Stop the servo encase its moving
        wiringpi.pwmWrite(pwmPin, stop)

        print "Servo: Command received = " + command

        #Act on the command
        if command == 'open':
            moveServo(4)
        elif command == '3quarter':
            moveServo(3)
        elif command == 'half':
            moveServo(2)
        elif command == 'quarter':
            moveServo(1)
        elif command == 'close':
            moveServo(0)

        return

    except KeyboardInterrupt:
        print('Interrupted')
        wiringpi.pwmWrite(pwmPin, stop)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
