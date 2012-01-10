import usb.core, usb.util, serial, time, copy, Queue
import threading, thread

timeout = 1
        
###############Master Class###############
#Handles all messages incoming from the various servo and motor classes, and adds them to the queueHandler
class Arduino(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.commandDict = {} 
        self.responseDict = {}
        self.commandQueue = Queue.Queue()
        self.lock = threading.Lock()
        self.portOpened = False
        self.killReceived = False #So a force quit will work

    def run(self):
        print "Connecting"
        self.portOpened = self.connect()
        #try:
        queueThread = threading.Thread(target=self.queueHandler())
        queueThread.start()
        #except Exception as errorText:
        #    print errorText

    def connect(self):
        if self.portOpened: self.close()
        try:
            self.port=serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
            #usb.core.find(idVendor=0x2341 idProduct=0x0042)
            time.sleep(2) #Allows the arduino to initialize
            self.port.flush()
        except:
            print "Arduino not connected"
            return False
        print "Connected"
        return True

    def close(self):
        if self.portOpened:
            self.port.flush()
            self.port.close()
            self.portOpened = False
            thread.exit()
        
    def addCommand(self, command, portNum, delay, waitForResponse): #Actuators get the command sent over and over
        #The port is used as a unique identifier, since it's counterproductive to be sending different commands to the same port
        #Delay exists because if there is no pause after a command is sent, the arduino effectively does nothing.
        #However, the best delay may be different between the different commands.
        self.lock.acquire()
        self.responseDict[portNum]=''
        self.commandDict[portNum] = [command,delay]
        self.lock.release()

        if waitForResponse:
            initTime = time.time()
            while ((self.responseDict[portNum]=='') and (time.time()-initTime<timeout)): time.sleep(0.001)
            return self.responseDict[portNum]

    def removeCommand(self,portNum):
        #Only required if you want the port to send no commands to the actuator at all
        #Add command changes the command being sent to the port, but isn't very good at removing a commands entirely

        self.lock.acquire()
        del self.commandDict[portNum]
        self.lock.release()

    def updateQueue(self):
        self.queue = Queue.Queue()
        #Can theoretically add a command while this is happening, thus the locking
        self.lock.acquire()
        for portNum,command in self.commandDict.iteritems():
            self.queue.put((portNum,command[0]))
        self.lock.release()

    def queueHandler(self):
        if not self.portOpened: thread.exit()
        while self.portOpened and not self.killReceived:
            
            self.updateQueue()
            while not self.queue.empty():
                self.lock.acquire()
                
                (portNum,command)=self.queue.get_nowait()
                if portNum not in self.commandDict:
                    self.lock.release()
                    continue
                
                delayParam = float(self.commandDict[portNum][1])

                self.lock.release()
                
                #Write Command
                self.port.flush()
                self.port.write(command)
                #print command

                #Pause so the arduino can process
                #time.sleep(delayParam) #<---maybe

                #Read from arduino
                fromArd = self.port.readline()
                self.responseDict[portNum]=fromArd #To make sure commandDict isn't changed by this thread
                #print fromArd
                

            self.portOpened=self.port.isOpen()
        
###############Servo Class###############
class Servo:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.portNum = _port

    def setAngle(self,angle):
        command ="S%(port)02d%(angle)03d" %{'port': self.portNum, 'angle':angle}
        self.arduino.addCommand(command, self.portNum, 0.1, False)

###############Analog Sensor Class###############
class AnalogSensor:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.portNum = _port

    def getValue(self): #Returns a voltage value
        command ="A%(port)02d" %{'port': self.portNum}
        value = self.arduino.addCommand(command, self.portNum, 0.05, True)
        if not value=='':
            voltageVal = int(value)*5.0/1023 #Converts the signal to a voltage
        else:
            voltageVal = -1000

        self.arduino.removeCommand(self.portNum)
        return voltageVal
        
###############Motor Class###############
class Motor:
    def __init__(self, _arduino, _num):
        self.arduino = _arduino
        self.motorNum = _num
        self.ID = "M{0}".format(_num)

    def setVal(self,val): #val between 0 and 127 (forward) or 200 and 327 (reverse). dependent on ArduinoBasicCommandDecoder.pde
        command ="M%(num)01d%(val)03d" %{'num': self.motorNum, 'val':val}
        self.arduino.addCommand(command, self.ID, 0.1, True)

###############Digital Sensor Class###############
class DigitalSensor:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.portNum = _port

    def getValue(self): #Returns a voltage value
        command ="D%(port)02d" %{'port': self.portNum}
        value = self.arduino.addCommand(command, self.portNum, 0.05, True)
        if not value=='':
            val = int(value)
        else:
            val = -1000

        self.arduino.removeCommand(self.portNum)
        return val
