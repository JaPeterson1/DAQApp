import mysql.connector
import random

class sqlConnection():
    """Class to manage connection with SQL server
    """
    def __init__(self, hostIP:str, username:str, password:str):
        self.database = mysql.connector.connect(host=hostIP,user=username,password=password)
        mycursor = self.database.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS daqdb")
        mycursor.execute("USE daqdb")
        mycursor.execute("CREATE TABLE IF NOT EXISTS datapoints \
                        (id INT AUTO_INCREMENT PRIMARY KEY, \
                        t1 TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                        solarPower1 FLOAT, \
                        solarPower2 FLOAT, \
                        windPower1 FLOAT, \
                        windPower2 FLOAT, \
                        loadPower FLOAT, \
                        windSpeed FLOAT, \
                        solarIntensity FLOAT)")
        self.database.commit()

    def addRow(self, solarPower1, solarPower2, windPower1, windPower2, loadPower, windSpeed, solarIntensity):
        """Send a row to the SQL server. 

        Args:
            solarPower1 (float): Solar power (W)
            solarPower2 (float): Solar power (W)
            windPower1 (float): Wind power (W)
            windPower2 (float): Wind power (W)
            loadPower (float): Power used (W)
            windSpeed (float): Speed of wind (m/s)
            solarIntensity (float): Intensity of light (kW/m^2)
        """
        cursor = self.database.cursor()
        vals = (solarPower1, solarPower2, windPower1, windPower2, loadPower, windSpeed, solarIntensity)
        cursor.execute("INSERT INTO datapoints (solarPower1, solarPower2, windPower1, windPower2, loadPower, windSpeed, solarIntensity) VALUES (%s, %s, %s, %s, %s, %s, %s)", vals)
        self.database.commit()