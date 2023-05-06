from arduino import arduino as arduinoHelper
from solarcharger import solarcharger
from solarchargerSim import solarcharger as solarChargerSim
from windTurbine1 import windTurbine
from apscheduler.schedulers.blocking import BlockingScheduler
from sql import sqlConnection
import constants
import time


solarCharger1 = solarcharger(constants.SOLAR_CHARGER_1_PORT)
solarCharger2 = solarChargerSim(constants.SOLAR_CHARGER_2_PORT)
windTurbine1 = windTurbine(constants.WIND_TURBINE_1_RADIUS_METERS, constants.WIND_TURBINE_1_EFFICIENCY, constants.WIND_TURBINE_1_AIR_DENSITY)
windTurbine2 = windTurbine(constants.WIND_TURBINE_2_RADIUS_METERS, constants.WIND_TURBINE_2_EFFICIENCY, constants.WIND_TURBINE_2_AIR_DENSITY)
arduino = arduinoHelper(constants.ARDUINO_PORT)
print("Connecting...")
time.sleep(5)

DB = sqlConnection(constants.SQL_HOST_IP, constants.SQL_USER_NAME, constants.SQL_PASSWORD)

def updateDB(database):
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
                database = sqlConnection(constants.SQL_HOST_IP, constants.SQL_USER_NAME, constants.SQL_PASSWORD)
            except:
                print("Failed to reconnect, retrying...", "Explanation: ", e)
                continue


scheduler = BlockingScheduler()
scheduler.add_job(updateDB, 'interval', seconds=constants.serverUpdateFrequency, args=(DB,))
scheduler.start()
print("Exiting")
