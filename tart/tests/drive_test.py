import sys, time
sys.path.append("/home/maslab-team-5/Maslab/tart/Libraries/")
from tart.arduino import arduino
from tart.logic import state_machine
from tart.world import mapping
from tart.control import pidrive
from tart.sensors import sensor
from tart.actuators import motor

if __name__ == "__main__":
    try:
        ard = arduino.ArduinoThread()
        map = mapping.Map(debug=True)
        drive = pidrive.PIDriveController(ard, map)
        ard.start()
        map.start()
        assert ard.waitReady()
        while True:
            drive.drive_to_point((100, 0))
    
    except KeyboardInterrupt:
        print "Ending Program"
    
    finally:
        try:
            map.stop()
            drive.stop()
            ard.stop()
        except:
            pass

