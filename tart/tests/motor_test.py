import sys, time, Tkinter
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.arduino import arduino

if __name__ == "__main__":
    try:
        ard=arduino.ArduinoThread(debug=True)
        ard.start()
        assert ard.waitReady()
        
        root=Tkinter.Tk()
        
        def makeCommand(motor):
            def setVal(val):
                motor.setValue(int(val))
            return setVal
        
        for i in range(1, 4):
            for j in range(2):
                motor=arduino.Motor(ard, (i, j))
                Tkinter.Label(root, text=str(i)+str(j)) \
                       .grid(row=0, column=2*i+j)
                Tkinter.Scale(root, to=-127, from_=127, resolution=1, \
                              command=makeCommand(motor))\
                       .grid(row=1, column=2*i+j)
        
        root.mainloop()
        
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        try:
            root.quit()
            ard.stop()
        except:
            pass
