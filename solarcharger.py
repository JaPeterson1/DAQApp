from solarshed.controllers.renogy_rover import RenogyRover
import threading
import time

class solarcharger:
    """Class to handle Renogy Rover charge controllers
    """
    def __init__(self, portname):
        """Create an instance of a Renogy Rover charge controller

        Args:
            portname (str): The /dev/USBXXX port the controller is in. 
        """
        self.controller = RenogyRover(portname=portname, slaveaddress = 1)
        self.dataQueue = []
        t = threading.Thread(target=self.updateThread)
        t.daemon = True
        t.start()


    def getSolarPower(self):
        """Get current solar power draw

        Returns:
            float: Watts
        """
        return self.controller.solar_power()
    
    def updateThread(self):
        """Looping thread that stores the power generated in an array every minute. 
        """
        while True:
            try:
                self.dataQueue.append(self.getSolarPower())
                if(len(self.dataQueue)>60):
                    self.dataQueue.pop(0)
            except Exception as e:
                print(e)
                continue
            time.sleep(60) #Sleep for 60s
    
    def poll(self): #get average hourly power
        """Get the average power across all the minute measurements.

        Returns:
            float: Watts
        """
        return sum(self.dataQueue)/len(self.dataQueue)