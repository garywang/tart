sys.path.append("Libraries/")
import arduino

class Motor(arduino.Motor):
    
    def setVal(self, val):
        realVal=val
        if(val<0):
            realVal=300-val
        arduino.Motor.setVal(self, realVal)