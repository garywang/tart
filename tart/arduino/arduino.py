import serial, time, threading

class ArduinoThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.commands = {}
        self.responses = {}
        self.lock = threading.Lock()
        self.port = None
        self.running = False
    
    def run(self):
        self.running = True
        self.connect()
        
        while self.port.isOpen() and self.running:
            #print "commands:", self.commands
            self.writeCommands()
            #print "responses:", self.responses
            self.readResponses()
            
        self.close()
    
    def connect(self):
        print "Connecting"
        for i in range(2):
            self.port = serial.Serial(port='/dev/ttyACM{0}'.format(i), baudrate=9600, timeout=0)
            if self.port.isOpen(): break
        else:
            print "Arduino not connected"
            return
        time.sleep(2) # Allows the arduino to initialize
        self.port.flush()
        print "Connected"
    
    def writeCommands(self):
        self.lock.acquire()
        for ID, command in self.commands.iteritems():
            self.port.write(command)
            time.sleep(0)
        self.lock.release()
        time.sleep(0)
            
    def readResponses(self):
        for line in self.port.readlines():
            response = line.strip().split(" ")
            if len(response) == 2:
                ID = response[0]
                self.responses[ID] = response[1]
            time.sleep(0)
        time.sleep(0)

    def close(self):
        if self.port.isOpen():
            self.port.flush()
            self.port.close()
    
    def waitReady(self): # Wait until connected
        while not self.port: time.sleep(0.001)
    
    def addCommand(self, ID, command, response):
        self.lock.acquire()
        self.commands[ID] = command
        self.lock.release()
        if response:
            self.responses[ID] = None
    
    def removeCommand(self, ID):
        self.lock.acquire()
        del self.commands[ID]
        if ID in self.responses:
            del self.responses[ID]
        self.lock.release()
    
    def updateCommand(self, ID, command): # Non locking version. can only be used to update existing keys
        if ID in self.commands:
            self.commands[ID] = command
        else:
            raise RuntimeError("attempted to update nonexistent command")
    
    def getResponse(self, ID):
        if ID in self.responses:
            while self.responses[ID] is None: time.sleep(0.001) # Wait for value to update
            return self.responses[ID]
        else:
            raise RuntimeError("attempted to get response to nonexistent command")
    
    def stop(self):
        self.running = False
            

class Servo:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.ID = "S{port:02d}".format(port=_port)
        self.arduino.addCommand(self.ID, "", False)

    def setAngle(self, angle):
        command = "{ID}{angle:03d}".format(ID=self.ID, angle=angle)
        self.arduino.updateCommand(self.ID, command)

class Motor:
    def __init__(self, _arduino, _num):
        self.arduino = _arduino
        self.ID = "M{num:01d}".format(num=_num)
        self.arduino.addCommand(self.ID, "", False)

    def setValue(self, value): # Value between -127 and 127
        command = "{ID}{value:+03d}".format(ID=self.ID, value=value)
        self.arduino.updateCommand(self.ID, command)

class AnalogSensor:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.ID = "A{port:02d}".format(port=_port)
        self.arduino.addCommand(self.ID, self.ID, True)

    def getValue(self): # Returns a voltage value
        value = self.arduino.getResponse(self.ID)
        voltage = int(value)*5.0/1023 # Converts the signal to a voltage
        return voltage

class DigitalSensor:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.ID = "D{port:02d}".format(port=_port)
        self.arduino.addCommand(self.ID, self.ID, True)

    def getValue(self):
        value = self.arduino.getResponse(self.ID)
        return int(value)


if __name__=="__main__":
    try:
        ard = ArduinoThread()
        #motor = Motor(ard,0)
        sensor = AnalogSensor(ard, 3)

        ard.start()
        ard.waitReady()

        #motor.setValue(127)
        print sensor.getValue()
        time.sleep(1)

        ard.close()
        
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.stop()
