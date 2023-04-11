from sql import sqlConnection
import time

SQL_HOST_IP = "192.168.50.2"
SQL_USER_NAME = "daq"
SQL_PASSWORD = "pass"


database = sqlConnection(SQL_HOST_IP, SQL_USER_NAME, SQL_PASSWORD)

print(database)
while(True):
    try:
        database.addRow(7,6,5,4,3,2,1)
        print("added row")
    except Exception as e:
        print(e)
        try:
            database = sqlConnection(SQL_HOST_IP, SQL_USER_NAME, SQL_PASSWORD)
        except Exception as e:
            print(e)
            continue
        database.addRow(7,6,5,4,3,2,1)
    time.sleep(10)