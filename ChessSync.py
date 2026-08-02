from flask import Flask, request, redirect, url_for, render_template, jsonify, send_file, Blueprint
from flask_mysqldb import MySQL
from io import StringIO,BytesIO
from Chess_api import *
from Chess_utilities import *
from Chess_db import *
import chess.pgn
import io

app = Flask(__name__)
app.register_blueprint(utilities_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/db/championship")
def db_menu():
    years = get_years()
    years.reverse()
    return render_template("db_menu.html", years=years)

@app.route("/db/championship/<year>")
def db_championship(year):
    championships_db = get_championships(year)
    championships = [(
            championship[0],
            format_championship(championship[2])
        )for championship in championships_db]
    return render_template("db_championships.html", year=year, championships=championships)

@app.route("/db/championship/<year>/<championship>/<int:id>")
def db_championship_games(year, championship, id):
    games = get_games(id)
    games = [{
            "event": game[2],
            "site": game[3],
            "date": game[4],
            "round": game[5],
            "white": game[6],
            "black": game[7],
            "result": game[8],
            "eco": game[9],
            "moves": game[10]
        }for game in games]

    return render_template("db_championships_games.html", year=year, championships=championship, games=games,db="db")

@app.route("/player/<name>")
def player_profile(name):
    profile = query_profile(name)
    stats = query_stats(name)

    if profile.status_code != 200:
        return render_template("error.html", message=f"Player for '{name}' not found!")

    pdata = profile.json()
    sdata = stats.json()

    return render_template("player.html", player=pdata, stats=sdata)

@app.route("/player/<name>/games")
def all_player_games(name):
    response = query_games(name)

    if response.status_code != 200:
        return render_template("error.html", message=f"Player for '{name}' not found!")

    data = response.json()
    archives = data.get("archives", [])

    months = []
    for url in archives:
        parts = url.rstrip("/").split("/")
        year, month = parts[-2], parts[-1]
        months.append({"year": year, "month": month})

    months.reverse()

    return render_template("game_history.html", name=name, months=months)

@app.route("/player/<name>/games/<year>/<month>")
def player_games(name, year, month):
    response = query_game(name, year, month)
    if response.status_code != 200:
        return render_template("error.html", message=f"Games for '{name}' not found!")

    data = response.json()
    games_data = data.get("games", [])
    if not games_data:
        return render_template("error.html", message="No games found.")

    games = []
    for game in games_data:
        pgn = game.get("pgn")
        chess_game = chess.pgn.read_game(StringIO(pgn))
        headers = chess_game.headers

        moves = []
        board = chess_game.board()
        for move in chess_game.mainline_moves():
            moves.append(board.san(move))
            board.push(move)

        games.append({
            "event": headers.get("Event", "Unknown"),
            "site": headers.get("Site", "Unknown"),
            "date": headers.get("Date", "Unknown"),
            "round": headers.get("Round", "Unknown"),
            "white": headers.get("White", "Unknown"),
            "black": headers.get("Black", "Unknown"),
            "result": headers.get("Result", "Unknown"),
            "eco": headers.get("ECO", "Unknown"),
            "moves": " ".join(moves),
        })

    return render_template("game_player.html", name=name, year=year, month=month, games=games,)

@app.route("/display-game", methods=["POST"])
def game_display():
    name = request.form.get("name")
    hdate = request.form.get("hdate")
    date = request.form.get("date", "????.??.??")
    round = request.form.get("round", "-")
    white = request.form.get("white", "White")
    black = request.form.get("black", "Black")
    result = request.form.get("result", "*")
    moves = request.form.get("moves", "")
    site = request.form.get("site", "")
    eco = request.form.get("eco", "")
    event = request.form.get("event", "")
    game_type = request.form.get("game_type", "")

    if game_type != "db":
        response = query_profile(name)
        if response.status_code != 200:
            return render_template("error.html", message=f"'{name}' not found!")

    pgn = io.StringIO(moves)
    chess_game = chess.pgn.read_game(pgn)

    if chess_game is None:
        return render_template("error.html", message=f"Game Not Found")

    STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    STARTING_POS = ""
    board = chess.Board()
    move_list = [STARTING_POS]
    positions = [STARTING_FEN]

    for move in chess_game.mainline_moves():
        san = board.san(move)
        move_list.append(san)
        board.push(move)
        positions.append(board.fen())

    game = {
        "name": name,
        "hdate": hdate,
        "date": date,
        "round": round,
        "white": white,
        "black": black,
        "result": result,
        "moves": move_list,
        "fen": positions,
        "site": site,
        "eco": eco,
        "event": event,
        "PGN_Moves": moves
    }

    return render_template("game_display.html", game=game,)

if __name__ == '__main__':
    app.run(debug=True)