import mysql.connector
from sqlTools.SQLLogin import *

connection = my_connection
cursor = connection.cursor()

all_years = """
    SELECT * FROM Dates;
"""

all_championships = """
    SELECT * FROM Championships WHERE year_value = %s;
"""

all_games = """
    SELECT * FROM Games WHERE championship_id = %s;
"""

def get_years():
    cursor.execute(all_years)
    return [row[0] for row in cursor.fetchall()]

def get_championships(year):
    cursor.execute(all_championships, (year,))
    return cursor.fetchall()

def get_games(id):
    id = int(id)
    cursor.execute(all_games, (id,))
    return cursor.fetchall()

def format_championship(name):
    names = {
        "WorldChamp": "World Championship",
        "FideChamp": "FIDE-Wch",
        "PCAChamp": "PCA-World Championship",
    }
    return names.get(name, name)