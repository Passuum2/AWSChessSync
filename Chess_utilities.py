from flask import Flask, request, redirect, url_for, render_template, jsonify, send_file, Blueprint
from flask_mysqldb import MySQL
from io import StringIO,BytesIO
from Chess_api import *
import chess.pgn
import json

utilities_bp = Blueprint("utilities_bp", __name__)

@utilities_bp.route("/search")
def search():
    username = request.args.get("api_search")
    return redirect(url_for("player_profile", name=username))

@utilities_bp.route("/search-player")
def search_player():
    username = (request.args.get("name") or "").lower()
    searched_player = (request.args.get("api_player_search") or "").lower()

    if not username or not searched_player:
        return "Missing 'name' or 'api_player_search' query parameter", 400

    archives = query_games(username).json()["archives"]
    matching_games = []

    for archive in archives:
        response = requests.get(archive, headers={"User-Agent": "Mozilla/5.0"})
        games = response.json()["games"]

        for game in games:
            white = game["white"]["username"].lower()
            black = game["black"]["username"].lower()

            if {white, black} != {username, searched_player}:
                continue

            pgn = game["pgn"]
            chess_game = chess.pgn.read_game(StringIO(pgn))
            headers = chess_game.headers
            board = chess_game.board()
            moves = []

            for move in chess_game.mainline_moves():
                moves.append(board.san(move))
                board.push(move)

            date_header = headers.get("Date", "Unknown")
            date_parts = date_header.split(".")
            if len(date_parts) >= 2 and date_parts[0].isdigit() and date_parts[1].isdigit():
                hdate = f"{date_parts[0]}/{date_parts[1]}"
            else:
                hdate = "unknown"

            matching_games.append({
                "event": headers.get("Event", "Unknown"),
                "site": headers.get("Site", "Unknown"),
                "date": date_header,
                "hdate": hdate,
                "round": headers.get("Round", "Unknown"),
                "white": headers.get("White", "Unknown"),
                "black": headers.get("Black", "Unknown"),
                "result": headers.get("Result", "Unknown"),
                "eco": headers.get("ECO", "Unknown"),
                "moves": " ".join(moves),
            })

    return render_template("player_search.html", name=username, searched_player=searched_player, games=matching_games,)

@utilities_bp.route("/saveGame", methods=["POST"])
def save_game():
    data = request.json
    moves = data.get("moves") if data else None
    if not moves:
        return jsonify({"error": "No moves provided"}), 400
    pgn_moves = " ".join(moves)
    file = BytesIO()
    file.write(pgn_moves.encode("utf-8"))
    file.seek(0)

    return send_file(
        file,
        as_attachment=True,
        download_name="line.pgn",
        mimetype="application/x-chess-pgn"
    )

@utilities_bp.route("/download", methods=["POST"])
def download_pgn():
    games = json.loads(request.form.get("games", "[]"))

    if not games:
        return "No games found."

    pgn_text = ""

    for game in games:
        pgn_text += f"""[Event "{game['event']}"]
[Site "{game['site']}"]
[Date "{game['date']}"]
[Round "{game['round']}"]
[White "{game['white']}"]
[Black "{game['black']}"]
[Result "{game['result']}"]
[ECO "{game['eco']}"]

{game['moves']}

"""

    file = BytesIO(pgn_text.encode("utf-8"))
    file.seek(0)

    return send_file(
        file,
        as_attachment=True,
        download_name="games.pgn",
        mimetype="application/x-chess-pgn"
    )

@utilities_bp.route("/download-game", methods=["POST"])
def download_game():
    event = request.form.get("event", "?")
    site = request.form.get("site", "?")
    date = request.form.get("date", "????.??.??")
    round = request.form.get("round", "-")
    white = request.form.get("white", "White")
    black = request.form.get("black", "Black")
    result = request.form.get("result", "*")
    eco = request.form.get("eco", "")
    moves = request.form.get("moves", "")

    def escape(value):
        return value.replace("\\", "\\\\").replace('"', '\\"')

    tags = [
        f'[Event "{escape(event)}"]',
        f'[Site "{escape(site)}"]',
        f'[Date "{escape(date)}"]',
        f'[Round "{escape(round)}"]',
        f'[White "{escape(white)}"]',
        f'[Black "{escape(black)}"]',
        f'[Result "{escape(result)}"]',
    ]
    if eco:
        tags.append(f'[ECO "{escape(eco)}"]')

    header_block = "\n".join(tags)
    pgn_text = f"{header_block}\n\n{moves} {result}\n"

    file = BytesIO()
    file.write(pgn_text.encode("utf-8"))
    file.seek(0)

    safe_date = date.replace(".", "-").replace("?", "x")

    return send_file(
        file,
        as_attachment=True,
        download_name=f"{white}_vs_{black}_{safe_date}.pgn",
        mimetype="application/x-chess-pgn"
    )

