import serial, time, threading, thread, math, sys
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart import params

class ArduinoThread(threading.Thread):
    
    def __init__(self, debug=params.arduino_debug):
        threading.Thread.__init__(self)
        self.commands = {}
        self.responses = {}
        self.lock = threading.Lock()
        self.port = None
        self.running = False
        self.connected = False
        self.debug = debug
    
    def run(self):
        self.running = True
        self.connect()
        
        while self.running and self.connected:
            if self.debug:
                print "Commands:", self.commands
                print "Responses:", self.responses
            self.loopCommands()
            time.sleep(0)
            
        self.running = False
        self.close()
    
    def connect(self):
        print "Connecting"
        for i in range(3):
            try:
                self.port = serial.Serial(port='/dev/ttyACM{0:01d}'.format(i), baudrate=9600, timeout=2)
                if self.port and self.port.isOpen():
                    break
            except serial.SerialException:
                continue

        if self.port and self.port.isOpen():
            time.sleep(2) # Allows the arduino to initialize
            self.port.flush()
            print "Connected"
            self.connected = True
        else:
            print "Arduino not connected"

    def loopCommands(self):
        self.lock.acquire()
        for ID, command in self.commands.iteritems():
            if command is not None:
                # write command
                self.port.write(command)
                if self.debug:
                    print "Sent:", repr(command)
                # block for response (don't flood the arduino with commands)
                response = self.port.readline().strip()
                if not response:
                    print "Response timeout"
                    self.stop()
                    break
                self.responses[ID] = response
                if self.debug:
                    print "Received:", repr(response)
                if ID[0] == 'S':
                    self.commands[ID] = None #Don't repeatedly send servo commands.
                time.sleep(0)
        self.lock.release()
    
    #This should not be called while the thread is still running
    def close(self):
        if self.port and self.port.isOpen():
            self.lock.acquire()
            self.port.flush()
            self.port.close()
            self.lock.release()
            self.connected = False
    
    def waitReady(self, timeout=10): # Wait until connected
        t = time.time()
        while time.time() - t < timeout and not self.connected: time.sleep(0.001)
        return self.connected
    
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
        self.arduino.addCommand(self.ID, "{ID}000".format(ID=self.ID), False)

    def setAngle(self, angle): # value between 0 and 180
        command = "{ID}{angle:03d}".format(ID=self.ID, angle=angle)
        self.arduino.updateCommand(self.ID, command)

class Motor:
    def __init__(self, _arduino, _id):
        self.arduino = _arduino
        self.ID = "M{controller:01d}{num:01d}".format(controller=_id[0], num=_id[1])
        self.arduino.addCommand(self.ID, "{ID}+000".format(ID=self.ID), False)

    def setValue(self, value): # value between -127 and 127
        val=int(math.floor(value+0.5))
        if val>127: val=127
        if val<-127: val=-127
        command = "{ID}{value:+04d}".format(ID=self.ID, value=val)
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

class Transistor:
    def __init__(self, _arduino, _port):
        self.arduino = _arduino
        self.ID = "T{port:02d}".format(port=_port)
        self.arduino.addCommand(self.ID, "{ID}0".format(ID=self.ID), False)

    def setValue(self, value): # value: 0 or 1
        command = "{ID}{value:01d}".format(ID=self.ID, value=value) 
        self.arduino.updateCommand(self.ID, command)

if __name__=="__main__":
    try:
        ard = ArduinoThread(debug=True)
        motor = Motor(ard, (1,0))
        #sensor = AnalogSensor(ard, 0)
        #servo = Servo(ard, 8)
        #transistor = Transistor(ard, 12)

        ard.start()
        assert ard.waitReady()

        motor.setValue(127)
        #transistor.setValue(1)
        for i in range(100):
            #print sensor.getValue()
            #servo.setAngle(i)
            time.sleep(0.1)
        #servo.setAngle(0)
        #transistor.setValue(0)
        time.sleep(1)
        
    #This is so that when you hit ctrl-C in the terminal, all the arduino threads close. You can do something similar with threads in your program.
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        ard.stop()
