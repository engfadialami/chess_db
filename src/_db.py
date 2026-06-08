import sqlite3
import pandas as pd

conn = sqlite3.connect("data/chess.db")

games_df = pd.read_csv("data/raw/chess_games.csv")
players_df = pd.read_csv("data/raw/player_registry.csv")

games_df.to_sql("games", conn, if_exists="replace", index=False)
players_df.to_sql("players", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("Database created successfully: data/chess.db")