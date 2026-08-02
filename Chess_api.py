import requests
from flask import Flask, send_file
import chess.pgn

PROFILE_URL = "https://api.chess.com/pub/player/{}"
STATS_URL = "https://api.chess.com/pub/player/{}/stats"
ALL_GAMES_URL = "https://api.chess.com/pub/player/{}/games/archives"
GAME_URL = "https://api.chess.com/pub/player/{}/games/{}/{}"
headers = {"User-Agent": "Mozilla/5.0"}

def query_profile(name):
    return requests.get(PROFILE_URL.format(name), headers=headers)

def query_games(name):
    return requests.get(ALL_GAMES_URL.format(name), headers=headers)

def query_stats(name):
    return requests.get(STATS_URL.format(name), headers=headers)

def query_game(name, year, month):
    return requests.get(GAME_URL.format(name, year, month),headers=headers)
