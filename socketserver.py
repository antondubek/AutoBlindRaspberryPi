
import socket
import sys
from thread import *
from servoController import servocontroller, getCurrentPosition

HOST = ''
PORT = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed'
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket listening on port ' + str(PORT)

def clientThread(conn):

    # conn.send('Welcome to Anthonys socket server\n')

    while True:

        # Get the sent request
        data = conn.recv(1024)

        print data

        # Save the data as an array
        dataArray = data.split("\n")

        # Split the first line of request
        firstLine = dataArray[0].split(" ")

        check = firstLine[0] #Save type of request
        command = firstLine[1] #Save the command
        command = command[1:] #Remove the / from beginning

        # If command is PUT, then set the blind
        if check == "PUT":
            print "check is = " + check
            print "Command to send = " + command

            if(command == "time"):

                #get the boolean
                timeOn = firstLine[2]

                #write to file
                file = open("config.txt", "w")

                if timeOn == "true":
                    toWrite = "true," + firstLine[3] + "," + firstLine[4]
                else:
                    toWrite = "false,0,0"

                file.write(toWrite)
                file.close()

            else:
                servocontroller(command)

        elif check == "GET":

            if command == "Time":
                #read enabled, timestart and finish from file
                file = open("config.txt", "r")
                reply = file.readline()

                #close the file
                file.close()

            elif command == "Position":
                reply = getCurrentPosition()

            print "Server response = " + reply
            conn.sendall(reply)

        break

    conn.close()

while 1:

    try:
        conn, addr = s.accept()
        print 'connected with ' + addr[0] + ':' + str(addr[1])

        start_new_thread(clientThread, (conn,))

    except KeyboardInterrupt:
        s.close()
        sys.exit
