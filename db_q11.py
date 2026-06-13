import sqlite3
import pandas as pd

conn = sqlite3.connect("data/processed/chess.db")

query = """
SELECT
    white_id,
    white_rating,
    game_id,

    RANK() OVER (
        PARTITION BY white_id
        ORDER BY white_rating DESC
    ) AS rating_rank

FROM games
LIMIT 10;
"""
# UNION CTE: combine white wins and black wins into one 'player_wins' table. Who has the most total wins?



result = pd.read_sql(query, conn)
print(result)
conn.close()

