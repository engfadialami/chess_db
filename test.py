import sqlite3
import pandas as pd

games = pd.read_csv("data/raw/chess_games.csv")

white_wins = (
    games[games["winner"]=="White"]
    .groupby("white_id")
    .size().sort_values(ascending=False)
)

print(white_wins)