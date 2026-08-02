## ChessSync
Chess Sync is a full-stack web analytics platform built with Python (Flask), MySQL, and Bootstrap. It imports, normalizes, and indexes a database of World Chess Championship games from 2000 to 2025, exposing the data through APIs and a responsive dashboard that aggregates and displays player statistics analysis.

## Contributors
NotSrihan - https://github.com/NotSrihan

## Features
**Historical Championship Data** (MySQL-backed)
- Imports and normalizes World Chess Championship game data (2000–2025)
- Indexed database for efficient querying by player, year, and opening (ECO code)

**Live Player Stats** (Chess.com API-backed)
- Account creation date
- Rapid/Blitz/Bullet ratings (best and current)
- Win/loss/draw record per time control
- Puzzle rating

**Game History & Head-to-Head Search** (Chess.com API-backed)
- Browse a player's full monthly game archive
- Search head-to-head games between two specific players
- Interactive move-by-move game viewer (chessboard.js)
- Download individual games or full month archives as PGN
    
## Screenshots
**Home Page** 

![Screenshot](Screenshots/Home-ChessSync-.png)

**API Stats Page**

![Screenshot](Screenshots/API-ChessSync-.png)

**Learn Page** 

![Screenshot](Screenshots/Learn-ChessSync-.png)

## Tech Stack
- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** Bootstrap, HTML/CSS

## Setup & Installation
### Prerequisites
- Python 3.x
- pip
- **Note:** Requires your own MySQL instance — see [Status](#status) below.

### Steps
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your own MySQL credentials
4. Set up MySQL database using `schema.sql`
5. Run the app: `python ChessSync.py`
6. Visit `http://localhost:5000` in your browser

## Project Structure
ChessSync.py       — main Flask app (routes for player profile, game history, and game viewer)

Chess_api.py       — Chess.com PubAPI request wrappers (profile, stats, games, archives)

Chess_utilities.py — Flask Blueprint with utility routes (head-to-head search, PGN downloads, save game)

templates/         — HTML views (index, player, game history, game viewer, search results, error)

static/css/        — styling

## Data Source
  Database: [PGNMentor](https://www.pgnmentor.com/files.html#world)

  PubAPI: https://support.chess.com/en/articles/9650547-what-is-the-pubapi-and-how-do-i-use-it

## Database Schema
See [`schema.sql`](./schema.sql) for full table definitions and relationships.

## Status
This project was originally built and tested using a university-provided MySQL instance, which is no longer active. The historical championship database features are not runnable without a live MySQL connection (see Setup). The live player stats lookup (via Chess.com API) does not depend on MySQL and should still function independently.

**Planned:** Migrating the database to AWS (RDS) with the app hosted on EC2 or Elastic Beanstalk, providing a live, publicly accessible version of the full dashboard.

