import serial, time, threading, thread

class ArduinoThread(threading.Thread):
    
    def __init__(self, debug=False):
        threading.Thread.__init__(self)
        self.commands = {}
        self.responses = {}
        self.lock = threading.Lock()
        self.port = None
        self.running = False
        self.debug = debug
    
    def run(self):
        self.running = True
        self.connect()
        
        while self.running and self.port.isOpen():
            if self.debug:
                print "Commands:", self.commands
                print "Responses:", self.responses
            self.loopCommands()
            time.sleep(0)
            
        self.close()
    
    def connect(self):
        print "Connecting"
        try:
            self.port = serial.Serial(port='/dev/ttyACM2', baudrate=9600, timeout=1)
            time.sleep(2) # Allows the arduino to initialize
            self.port.flush()
        except serial.SerialException:
            self.stop()
            raise
        print "Connected"
    
    def loopCommands(self):
        self.lock.acquire()
        for ID, command in self.commands.iteritems():
            # write command
            self.port.write(command)
            if self.debug:
                print "Sent:", command
            # block for response (don't flood the arduino with commands)
            response = self.port.readline().strip()
            self.responses[ID] = response
            if self.debug:
                print "Received:", response
            time.sleep(0)
        self.lock.release()
    
    #This should not be called while the thread is still running
    def close(self):
        if self.port.isOpen():
            self.port.flush()
            self.port.close()
    
    def waitReady(self): # Wait until connected
        while self.running and not self.port: time.sleep(0.001)
        return self.running
    
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
    

Arduino=ArduinoThread

class Servo:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.ID = "S{port:02d}".format(port=_port)
        self.arduino.addCommand(self.ID, "", False)

    def setAngle(self, angle):
        command = "{ID}{angle:03d}".format(ID=self.ID, angle=angle)
        self.arduino.updateCommand(self.ID, command)

class Motor:
    def __init__(self, _arduino, _controller, _num):
        self.arduino = _arduino
        self.ID = "M{controller:01d}{num:01d}".format(controller=_controller, num=_num)
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
        ard = ArduinoThread(debug=True)
        motor = Motor(ard, 1, 0)
        #sensor = AnalogSensor(ard, 0)

        ard.start()
        success = ard.waitReady()
        if not success: thread.exit()

        motor.setValue(127)
        for i in range(100):
            #print sensor.getValue()
            time.sleep(0.1)
        
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.stop()
