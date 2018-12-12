
import socket
import sys
from thread import *
from servoController import servocontroller, getCurrentPosition

HOST = '' #Blank for localhost
PORT = int(sys.argv[1]) #Get port from first argument passed

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind the socket to the host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed'
    sys.exit()

print 'Socket bind complete'

# Listen for connections on the socket
s.listen(10)
print 'Socket listening on port ' + str(PORT)


#Parses the connection retrieving commands and sending requests to servo controller
def clientHandler(conn):

    # Wait for a request to be passed
    while True:

        # Get the sent request
        data = conn.recv(1024)

        # Save the data as an array
        dataArray = data.split("\n")

        # Split the first line of request
        firstLine = dataArray[0].split(" ")

        check = firstLine[0] #Save type of request
        command = firstLine[1] #Save the command
        command = command[1:] #Remove the / from beginning

        # If command is POST, then set the time or send to servocontroller
        if check == "POST":
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

# Forever, check for connections to the server
while 1:

    try:
        conn, addr = s.accept()
        print 'connected with ' + addr[0] + ':' + str(addr[1])

        #When have a connection, create a connection handler and pass the connection
        start_new_thread(clientHandler, (conn,))

    except KeyboardInterrupt:
        s.close()
        sys.exit
