
import SimpleHTTPServer
import SocketServer
import logging
import cgi
import serial
import sys
import json
import signal
import time

PORT = 3000
planted = False
myinst = 0
#If we ctrl+C out of python, make sure we close the serial port first
#handler catches and closes it
def signal_handler(signal, frame):
    ser.close()
    sys.exit(0)



class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


    #SimpleHTTPServer doesn't handle post by default. Hacked up way to do it here
    def do_POST(self):
        global myinst
        time.sleep(0.3)
        length = int(self.headers["Content-Length"])
        jsonString = str(self.rfile.read(length))
        #print jsonString
        print myinst
        myinst = myinst + 1
        jsonDict = json.loads(jsonString)
        #From here we have a JSON dict, that has whatever data CS is sending
        #fo.write(str(myinst))
        #For the timer, all we care about is the the 'round' key

        if 'round' in jsonDict:
            rounds = jsonDict['round']
            if 'bomb' in rounds:
                #print myinst
                #If bomb has been planted, then send the 'P' message
                if rounds['bomb'] == "planted":
                    planted = True
                    #print "Bomb has been planted"
                    #fo.write("P9\n")
                    ser.write('P')
                #If bomb has been defused, then send the 'C' message
                if rounds['bomb'] == "defused":
                    planted = False
                    ser.write('C')
                    #fo.write("C9\n")
                    print ("bomb has been defused")

            if 'phase' in rounds:
                if rounds['phase'] == "over":
                    planted = False
                    ser.write('C')
                    print ("Time Over")

            #if the round ends, either bomb exploded or everyone died.
            #Send the 'C' message to stop timer.
            if 'previously' in jsonDict:
                if 'round' in jsonDict['previously']:
                    if 'bomb' in jsonDict['previously']['round']:
                        planted = False
                        print ("Round ran out")
                        #fo.write("Round ran out\n")
                        ser.write('C')




Handler = ServerHandler
#On windows, Serial ports are usually COM1-3
#On mac/linux this will be different
ser = serial.Serial('COM5')
#Set up our handler for ctrl+c
signal.signal(signal.SIGINT, signal_handler)
#fo = open("foo23.txt", "wb")
#Start server
httpd = SocketServer.TCPServer(("127.0.0.1", PORT), Handler)


#Run server
httpd.serve_forever()
