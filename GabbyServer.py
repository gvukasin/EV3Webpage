#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir,sep,listdir
import os,sys
import cgi
import thread
import threading
import time

info = True
BotSpeak = []
VAR = {'VER':0.1, 'HI':1, 'LO':0}

# motor dictionary
MOTORS = {}

# sensor dictionary
SENSORS = {}


PORT_NUMBER = input('set port  number:')



####### linux path names on EV3DEV #######
#motor definitions
motorAttached = '/sys/class/tacho-motor/'
motorpath = '/sys/class/tacho-motor/{}/'
setMotorSpeed = motorpath + 'duty_cycle_sp'
runMotor = motorpath + 'command'

# check if this is true 
checkMotorPort = motorpath + 'port_name' 

#LED definitions

ledpath = '/sys/class/leds/ev3-{}:{}:ev3dev/'
ledbright = ledpath +'brightness'

#sensor definitions

sensorpath = '/sys/class/lego-sensor/{}/'
sensorValue = sensorpath + 'value0'
sensorAttached = '/sys/class/lego-sensor/'
checkSensorPort = sensorpath + 'port_name'
drivername = sensorpath + 'driver_name'

ultrasonicpath = 'ev3-uart-30'
ultrasonicmode = 'US-DIST-CM'
ultrasonicvalue = 'value0'

gyroname = 'ev3-uart-32' 
gyromode = 'GYRO-ANGLE'
gyrovalue = 'value0'

touchname = 'ev3-touch'
touchmode = 'TOUCH'
touchvalue = 'value0'

irname = 'ev3-uart-33'
irmode = 'IR-PROX'
irvalue = 'value0'

analogname = 'ev3-analog'
analogvalue = 'value0'



#This class will handles any incoming request from the browser 
class myHandler(BaseHTTPRequestHandler):
        
        #Handler for the GET requests
        def do_GET(self):
                print self.path
                if self.path=="/":
                        self.path="/Ev3devWebpage.html"

                elif self.path.startswith('/sensor'):
                        # sensor dictionary {'actual Ev3 port':'sensor0'}
                        existingSensors = os.listdir(sensorAttached)
                        print existingSensors
                        print len(existingSensors)

                        SENSORS = {} # reset dictionary

                        for i in range(0,len(existingSensors)):
                                try:
                                        senRead = open(checkSensorPort.format(existingSensors[i])) 
                                        print senRead
                                        mo = senRead.read()
                                        print mo
                                        senRead.close
                                        SENSORS[mo[2]] = existingSensors[i] # add to dictionary
                                except IOError:
                                        print "no sensor"
                        print SENSORS

                        for i in range(0,len(existingSensors)):
                                # read sensor value
                                n = str(i+1)
                                Sens = open(sensorValue.format(SENSORS[n]))
                                theValue = Sens.read()
                                Sens.close
                                print theValue

                                # ask what sensor is plugged in - theSensor
                                # FIX THIS PERMISSION DENIED (ERROR 13) 
                                sensor = open(drivername.format(SENSORS[n]),'r+')
                                theSensor = sensor.read()
                                sensor.close
                                print theSensor

# send back sensor values to spaces on webpage
                                # ultrasonic sensor
                                if theSensor == 'ev3-uart-30':
                                        print 'ultrasonic sensor'
                        
                                # gyro sensor   
                                elif theSensor == 'ev3-uart-32':
                                        print 'gyro sensor'
                                        

                                # touch sensor 
                                elif theSensor == 'ev3-touch':
                                        print 'touch sensor'
                                       

                                # ir sensor 
                                elif theSensor == 'ev3-uart-33':
                                        print 'IR sensor'
                                   
                                        
                                # angle sensor
                                elif theSensor == 'ev3-analog':
                                        print 'angle sensor'
                              

                                        
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write("success")

                       

                try:
                        #Check the file extension required and
                        #set the right mime type

                        sendReply = False
                        if self.path.endswith(".html"):
                                mimetype='text/html'
                                sendReply = True
                        if self.path.endswith(".jpg"):
                                mimetype='image/jpg'
                                sendReply = True
                        if self.path.endswith(".gif"):
                                mimetype='image/gif'
                                sendReply = True
                        if self.path.endswith(".js"):
                                mimetype='application/javascript'
                                sendReply = True
                        if self.path.endswith(".css"):
                                mimetype='text/css'
                                sendReply = True

                        if sendReply == True: 
                                #Open the static file requested and send it
                                f = open(curdir + sep + self.path) 
                                self.send_response(200)
                                self.send_header('Content-type',mimetype)
                                self.end_headers()
                                self.wfile.write(f.read())
                                f.close()
                        return          
                except IOError:
                        self.send_error(404,'File Not Found: %s' % self.path)

        #Handler for the POST requests
        def do_POST(self):
                print self
                print self.path
                
                if self.path=="/motor":
                        form = cgi.FieldStorage(
                                fp=self.rfile, 
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],}
                        )
                        
                        print form


                        # motor dictionary {'actual Ev3 port':'motor0'}
                        existingMotors = os.listdir(motorAttached)
                        print existingMotors
                        print len(existingMotors)

                        MOTORS = {} # reset dictionary

                        for i in range(0,len(existingMotors)):
                                try:
                                        motorRead = open(checkMotorPort.format(existingMotors[i])) 
                                        print motorRead
                                        mo = motorRead.read()
                                        print mo
                                        motorRead.close
                                        MOTORS[mo[3]] = existingMotors[i] # add to dictionary
                                except IOError:
                                        print "no motor"
                        print MOTORS

                        # set speeds and run motors that exist
                        for i in range(0,3):
                                port = changePort(i)
                                print port
                                if port in MOTORS: # if motor exists in port 
                                        speed = 'Speed{}'.format(i)
                                        motor = open(setMotorSpeed.format(MOTORS[port]),"w",0)
                                        motor.write(form[speed].value + '\n')
                                        motor.close
                                        motor = open(runMotor.format(MOTORS[port]),"w",0)
                                        if form['cmd'].value == 'run': #run motor 
                                                motor.write('run-forever')
                                        else:# stop motor
                                                motor.write('stop')
                                        motor.close
                                
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write("success")
                        return                  

                if self.path=="/led":
                        form2 = cgi.FieldStorage(
                                fp=self.rfile, 
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                 'CONTENT_TYPE':self.headers['Content-Type'],
                        })
                        
                        print form2
                        
                        if form2['cmd'].value == 'update':
                                LED = open(ledbright.format('right0','red'),"w",0)
                                LED.write(form2['LEDRR'].value + '\n')
                                LED.close
                                LED = open(ledbright.format('left0','red'),"w",0)
                                LED.write(form2['LEDLR'].value + '\n')
                                LED.close
                                LED = open(ledbright.format('right1','green'),"w",0)
                                LED.write(form2['LEDRG'].value + '\n')
                                LED.close
                                LED = open(ledbright.format('left1','green'),"w",0)
                                LED.write(form2['LEDLG'].value + '\n')
                                LED.close

                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write("success")
                        return                  

                if self.path=="/BotSpeak":
                        form3 = cgi.FieldStorage(
                                fp=self.rfile, 
                                headers=self.headers,
                                environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],}
                        )
                        
                        print form3
                        
                        global BotSpeak 
                        BotSpeak = form3['BotSpeak'].value.split('\r\n')
                        
                                      
# This is a thread that runs the web server 
def WebServerThread():                  
        try:
                #Create a web server and define the handler to manage the
                #incoming request
                server = HTTPServer(('', PORT_NUMBER), myHandler)
                print 'Started httpserver on port ' , PORT_NUMBER
                
                #Wait forever for incoming htto requests
                server.serve_forever()

        except KeyboardInterrupt:
                print '^C received, shutting down the web server'
                server.socket.close()


# Runs the web server thread
thread.start_new_thread(WebServerThread,())             


def PWM(channel,value):
        port=int(channel)
        if value.isdigit():
                speed = float(value)
        else: speed = float(VAR[value])
        print ('Setting PWM {} to {}').format(port,speed)
        return speed

def AI(value):
        return 1024
        
OPS = {'PWM':PWM, 'AI':AI}

#Execute BotSpeak Command
def ExecuteCommand(command):
        if command == '':
                return command
        cmd,space,value = command.partition(' ')
        channel = '0'
        source = ''
        if ',' in value:
                source,space,value = value.partition(',')
        if '[' in source:
                source,space,channel = source.partition('[')
                print channel
                channel = channel.split(']')[0]
        if (source == 'AO'): source = 'PWM'
        if cmd == 'SET':
                print 'Setting '+source+' [' + channel + '] to ' + value
                
                OPS[source] (channel,value)
#               if (source == 'PWM'):  PWM(source, value)
#               elif (source == '
#               exec('%s = %f' % (source,float(value)))
                return value
        elif cmd == 'GET':
                return value
        elif cmd == 'WAIT':
                waitTime = float(value) / 1000
                time.sleep(waitTime)
                return value

# port 0,1,2,3 to A,B,C,D
def changePort(portNum):
        if portNum in range(0,3):
                if portNum == 0:
                        value = 'A'
                elif portNum == 1:
                        value = 'B'
                elif portNum == 2:
                        value = 'C'
                elif portNum == 3:
                        value = 'D'
                else:
                        value = ''
                return value

                

while True:
        time.sleep(0.5)
                
