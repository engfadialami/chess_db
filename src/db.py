import sqlite3
import pandas as pd

conn = sqlite3.connect("data/chess.db")

games = pd.read_csv("data/raw/chess_games.csv")
players = pd.read_csv("data/raw/player_registry.csv")

games.to_sql("games", conn, if_exists="replace", index=False)
players.to_sql("players", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database created successfully: data/chess.db")