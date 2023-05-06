import serial
import time
import threading
import constants

class arduino:
    def __init__(self, port):
        """Create an instance of the arduino reading class. 

        Args:
            port (str): The /dev/ACMXXX port the arduino is plugged in on. 
        """
        self.port = port
        self.solarIntensity = []
        self.windSpeed = []
        self.loadPower = []
        self.serial = serial.Serial(port, 115200)
        self.serial.reset_input_buffer()
        #t = threading.Thread(target=self.updateThread)
        #t.daemon = True
        #t.start()
    
    def sendSerial(self, msg):
        """Send a message over serial. 

        Args:
            msg (str): message contents
        """
        self.serial.write(msg.encode('utf8'))
    
    def getSerial(self):
        """Read a line from serial. Blocks until a new line is read.

        Returns:
            str: byte string with the line.
        """
        res = self.serial.readline()
        return res

    def updateData(self):
        """Send a message over serial and read the response.

        Returns:
            str: response string
        """
        self.sendSerial('\n')
        res = self.getSerial().decode()
        return res

    def pollSolarIntensity(self):
        """Get the average solar intensity over the last hour. 

        Returns:
            float: kW/m^2
        """
        return sum(self.solarIntensity)/len(self.solarIntensity)
    
    def pollWindSpeed(self):
        """Get the average wind speed over the last hour.

        Returns:
            float: m/s
        """
        return sum(self.windSpeed)/len(self.windSpeed)
    
    def pollLoadPower(self):
        """Get the average power draw over the last hour.

        Returns:
            float: Watts
        """
        return sum(self.loadPower)/len(self.loadPower)

ard = arduino('/dev/ttyACM0')
ard.sendSerial('\n')
while True:
   ard.updateData()
   print(ard.updateData())