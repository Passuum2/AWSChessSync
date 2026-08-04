## ChessSync
Full-stack chess web app built with Flask & MySQL — Chess.com API integration, player head-to-head search, a browsable championship game database, and PGN downloads with an interactive board.

## Contributors
NotSrihan - https://github.com/NotSrihan

## Features
**Historical Championship Database** (MySQL-backed)
- Imports and normalizes World Chess Championship game data (1886–2024)
- Browse by year → championship → full game list, ordered chronologically
- Indexed database for efficient querying by player, year, and opening (ECO code)
- Download individual games or mass-download all games in a championship as PGN

**Live Player Stats** (Chess.com API-backed)
- Account creation date
- Title
- Rapid/Blitz/Bullet ratings
- Win/loss/draw record per time control

**Game History & Head-to-Head Search** (Chess.com API-backed)
- Browse a player's full monthly game archive
- Search head-to-head games between two specific players
- Interactive move-by-move game viewer (chessboard.js) with a clickable moves list — click any move to jump the board directly to that position
- Download individual games, or mass-download all displayed games (by month or by player matchup) as PGN

**Explore Board** (Home page)
- Freeform interactive chessboard for playing out lines
- Move list panel with undo/clear controls
- Save and download the current line as a PGN

## Screenshots
**Home Page**

![Screenshot](Screenshots/Home-ChessSync-.png)

**API Stats Page**

![Screenshot](Screenshots/API-ChessSync-1.png)

![Screenshot](Screenshots/API-ChessSync-2.png)

![Screenshot](Screenshots/API-ChessSync-3.png)

![Screenshot](Screenshots/API-ChessSync-4.png)

**Championship Database**

![Screenshot](Screenshots/DB-ChessSync-1.png)

![Screenshot](Screenshots/DB-ChessSync-2.png)

![Screenshot](Screenshots/DB-ChessSync-3.png)

**Display Board**

![Screenshot](Screenshots/DisplayBoard-ChessSync-.png)

## Tech Stack
- **Backend:** Python, Flask (Blueprint-based routing)
- **Database:** MySQL
- **REST API:** Chess.com PubAPI (JSON, unauthenticated GET requests)
- **Frontend:** HTML/CSS (custom stylesheet, chessboard.js, chess.js)
- **Deployment (planned):** AWS RDS + EC2

## Setup & Installation
### Prerequisites
- Python 3.x
- pip
- **Note:** Requires your own MySQL instance — see [Status](#status) below.

### Steps
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `env.example` to `.env` and fill in your own MySQL credentials
4. Set up the MySQL database using the `sqlTools/` scripts (see [Database Setup](#database-setup) below)
5. Run the app: `python ChessSync.py`
6. Visit `http://localhost:5000` in your browser

## Project Structure
```
ChessSync.py         — main Flask app (routes for player profile, game history, championship DB, game viewer)
Chess_db.py          — MySQL query layer (cursor/execute wrappers for pulling championship and game data)
Chess_api.py          — Chess.com PubAPI request wrappers (profile, stats, games, archives)
Chess_utilities.py    — Flask Blueprint with utility routes (head-to-head search, PGN downloads, save game)
sqlTools/
  createdatabase.py   — builds table structure and imports data from database/*.csv
  deletedatabase.py   — drops all tables
  SQLlogin.py          — loads MySQL credentials from .env (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
database/            — source CSV files for the championship dataset
templates/            — HTML views (home, player, game history, championship DB, game viewer, search results, error)
static/css/main.css   — shared stylesheet
static/js/            — chessboard.js and supporting scripts
```

## Data Source
Database: [PGNMentor](https://www.pgnmentor.com/files.html#world)

PubAPI: https://support.chess.com/en/articles/9650547-what-is-the-pubapi-and-how-do-i-use-it

## Database Setup
The championship database is built from CSV files and Python scripts:

1. Add your MySQL credentials to `.env` (see [Setup](#setup--installation) above) — `sqlTools/SQLlogin.py` reads them from there
2. Run `python sqlTools/createdatabase.py` — this reads every CSV in `sqlTools/database/` and automatically creates the corresponding table structure, then imports the data
3. To reset, run `python sqlTools/deletedatabase.py` to drop all tables, then re-run `createdatabase.py`

## Status
This project was originally built and tested using a university-provided MySQL instance, which is no longer active. The historical championship database features are not runnable without a MySQL connection (see Setup).

**In progress:** Migrating the database to AWS (RDS) with the app hosted on EC2, to provide a live, publicly accessible version of the full dashboard.
