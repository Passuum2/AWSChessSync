from pathlib import Path
import mysql.connector
import pandas as pd
from SQLLogin import *

connection = my_connection
cursor = connection.cursor()

cursor.execute(
    "DROP TABLE Games;"
)

cursor.execute(
    "DROP TABLE Championships;"
)

cursor.execute(
    "DROP TABLE Dates;"
)

connection.commit()
cursor.close()
connection.close()