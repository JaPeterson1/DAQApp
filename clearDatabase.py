import constants
from sql import sqlConnection

DB = sqlConnection(constants.SQL_HOST_IP, constants.SQL_USER_NAME, constants.SQL_PASSWORD)
DB.runCommand("DELTE * FROM datapoints")

print("Successfully cleared database.")