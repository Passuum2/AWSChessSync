from pathlib import Path
import mysql.connector
import pandas as pd
from SQLLogin import *

connection = my_connection
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE Dates (
        year_value INT NOT NULL PRIMARY KEY,
        CHECK (year_value BETWEEN 1000 AND 9999)
    );
    """
)

cursor.execute(
    """
    CREATE TABLE Championships (
        championship_id INT AUTO_INCREMENT PRIMARY KEY,
        year_value INT NOT NULL,
        championship_type VARCHAR(100) NOT NULL,
        FOREIGN KEY (year_value) REFERENCES Dates(year_value)
    );
    """
)

cursor.execute(
    """
    CREATE TABLE Games (
        game_id INT AUTO_INCREMENT PRIMARY KEY,
        championship_id INT,
        event VARCHAR(100),
        site VARCHAR(100),
        game_date VARCHAR(20),
        round VARCHAR(20),
        white VARCHAR(100),
        black VARCHAR(100),
        result VARCHAR(10),
        eco VARCHAR(5),
        moves TEXT,
        FOREIGN KEY (championship_id) REFERENCES Championships(championship_id)
    );
    """
)

database_path = Path("C:/Users/MDari/OneDrive/Desktop/AWSChessSync/database/")

years = []
championships = []
games = []

for files in database_path.iterdir():
    file_year = ""
    file_type = ""

    games_df = pd.read_csv(files)

    for char in files.stem:
        if char.isdigit():
            file_year += char
        else:
            file_type += char

    if file_year and file_type:
        years.append(int(file_year))
        championships.append(file_type)
        games.append(games_df)

df = pd.DataFrame({
    "year": years,
    "championship": championships,
    "games": games
})

df = df.groupby("year").agg({
    "championship": list,
    "games": list
}).reset_index()

for _, row in df.iterrows():
    year = row["year"]

    cursor.execute(
        "INSERT INTO Dates (year_value) VALUES (%s)",
        (year,)
    )

    for i, championship in enumerate(row["championship"]):

        cursor.execute(
            "INSERT INTO Championships (year_value, championship_type) VALUES (%s, %s)",
            (year, championship)
        )

        championship_id = cursor.lastrowid

        games_df = row["games"][i]

        for _, game in games_df.iterrows():
            game = game.where(pd.notna(game), None)
            cursor.execute(
                """
                INSERT INTO Games 
                (championship_id, event, site, game_date, round, white, black, result, eco, moves)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    championship_id,
                    game["Event"],
                    game["Site"],
                    game["Date"],
                    game["Round"],
                    game["White"],
                    game["Black"],
                    game["Result"],
                    game["ECO"],
                    game["Moves"]
                )
            )
connection.commit()
cursor.close()
connection.close()