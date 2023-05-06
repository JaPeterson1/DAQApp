class solarcharger:
    def __init__(self, portname):
        """Create an instance of a Renogy Rover charge controller

        Args:
            portname (str): The /dev/USBXXX port the controller is in. 
        """
    
    def poll(self): #get average hourly power
        """Get the average power across all the minute measurements.

        Returns:
            float: Watts
        """
        return 0
