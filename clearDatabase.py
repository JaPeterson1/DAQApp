import constants
from sql import sqlConnection
import mysql.connector


db = mysql.connector.connect(host=constants.SQL_HOST_IP, user = constants.SQL_USER_NAME, password=constants.SQL_PASSWORD)
cur = db.cursor()
cur.execute("USE daqdb")
cur.execute("DELETE FROM datapoints")
db.commit()
print("Successfully cleared database.")
