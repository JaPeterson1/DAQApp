from arduino import arduino as arduinoHelper
from solarcharger import solarcharger
from windTurbine1 import windTurbine
from apscheduler.schedulers.blocking import BlockingScheduler
from sql import sqlConnection

SQL_HOST_IP = "192.168.50.2"
SQL_USER_NAME = "daq"
SQL_PASSWORD = "pass"

ARDUINO_PORT = "/dev/ttyACM0"
SOLAR_CHARGER_1_PORT = "/dev/ttyUSB0"
SOLAR_CHARGER_2_PORT = "/dev/ttyUSB1"

WIND_TURBINE_1_EFFICIENCY = .2 #*100%
WIND_TURBINE_1_RADIUS_METERS = 1 #m
WIND_TURBINE_1_AIR_DENSITY = 1.2 #kg/m^3

WIND_TURBINE_2_EFFICIENCY = .05 #*100%
WIND_TURBINE_2_RADIUS_METERS = 1 #m
WIND_TURBINE_2_AIR_DENSITY = 1.2 #kg/m^3

solarCharger1 = solarcharger(SOLAR_CHARGER_1_PORT)
solarCharger2 = solarcharger(SOLAR_CHARGER_2_PORT)
arduino = arduinoHelper(ARDUINO_PORT)
windTurbine1 = windTurbine(WIND_TURBINE_1_RADIUS_METERS, WIND_TURBINE_1_EFFICIENCY, WIND_TURBINE_1_AIR_DENSITY)
windTurbine2 = windTurbine(WIND_TURBINE_2_RADIUS_METERS, WIND_TURBINE_2_EFFICIENCY, WIND_TURBINE_2_AIR_DENSITY)

database = sqlConnection(SQL_HOST_IP, SQL_USER_NAME, SQL_PASSWORD)

def updateDB():
    """Attempts to send the latest data for all sensors to the server until it succeeds. Should be run periodically.
    """
    while True:
        loadPower = arduino.pollLoadPower()
        windSpeed = arduino.pollWindSpeed()
        solarIntensity = arduino.pollSolarIntensity()
        solar1Power = solarCharger1.poll()
        solar2Power = solarCharger2.poll()
        wind1Power = windTurbine1.getPower(windSpeed)
        wind2Power = windTurbine2.getPower(windSpeed)
        try:
            database.addRow(solar1Power, solar2Power, wind1Power, wind2Power, loadPower, windSpeed, solarIntensity)
        except:
            try:
                database = sqlConnection(SQL_HOST_IP, SQL_USER_NAME, SQL_PASSWORD)
            except:
                continue


scheduler = BlockingScheduler()
scheduler.add_job(updateDB, 'interval', hours=1)