from arduino import arduino as arduinoHelper
from solarchargerSim import solarcharger
from windTurbine1 import windTurbine
from apscheduler.schedulers.blocking import BlockingScheduler
from sql import sqlConnection
from constants import *


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
        print("Running hourly fetch...")
        loadPower = arduino.pollLoadPower()
        windSpeed = arduino.pollWindSpeed()
        solarIntensity = arduino.pollSolarIntensity()
        solar1Power = solarCharger1.poll()
        solar2Power = solarCharger2.poll()
        wind1Power = windTurbine1.getPower(windSpeed)
        wind2Power = windTurbine2.getPower(windSpeed)
        print("Sending row:", solar1Power, solar2Power, wind1Power, wind2Power, loadPower, windSpeed, solarIntensity)
        try:
            database.addRow(solar1Power, solar2Power, wind1Power, wind2Power, loadPower, windSpeed, solarIntensity)
            break
        except Exception as e:
            print("Failed to send, attempting reconnection...", "Explanation: ", e)
            try:
                database = sqlConnection(SQL_HOST_IP, SQL_USER_NAME, SQL_PASSWORD)
            except:
                print("Failed to reconnect, retrying...", "Explanation: ", e)
                continue


scheduler = BlockingScheduler()
scheduler.add_job(updateDB, 'interval', seconds=serverUpdateFrequency)
scheduler.start()
print("Exiting")