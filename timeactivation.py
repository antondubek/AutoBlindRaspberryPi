# File will be ran as a cronjob

from datetime import datetime

#get the system time
now = datetime.now()
hour = now.hour
minute = now.minute

#get the time and boolean from the files
file = open("config.txt", "r")
line = file.readline()
file.close()

lineArray = line.split(",")
enabled = lineArray[0]
openTime = lineArray[1]
closeTime = lineArray[2]

openHour = int(openTime[:2])
openMinute = int(openTime[2:])
closeHour = int(closeTime[:2])
closeMinute = int(closeTime[2:])

#Check the boolean
if enabled == "true":
    #Check to see if time is within same minute as system time and hour the same
    if hour == openHour and minute == openMinute:
        #Check the position of the blind
        #Open / close if neccassary
        print "Open Loop"
    elif hour == closeHour and minute == closeMinute:
        #Check the position of the blind
        #Open / close if neccassary
        print "Close loop"
