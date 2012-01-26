import sys, time, Tkinter
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.arduino import arduino

if __name__ == "__main__":
    try:
        ard=arduino.ArduinoThread(debug=True)
        ard.start()
        assert ard.waitReady()
        
        root=Tkinter.Tk()
        
        def makeCommand(servo):
            def setVal(val):
                servo.setAngle(int(val))
            return setVal
        
        for i in range(8, 12):
            servo=arduino.Servo(ard, i)
            Tkinter.Label(root, text=str(i)) \
                   .grid(row=0, column=i)
            Tkinter.Scale(root, to=0, from_=180, resolution=1, \
                          command=makeCommand(servo))\
                   .grid(row=1, column=i)
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        try:
            root.quit()
            ard.stop()
        except:
            pass
