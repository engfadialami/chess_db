
import sqlite3
import pandas as pd

conn = sqlite3.connect("data/processed/chess.db")

query = """
SELECT
    white_id,
    game_id,
    white_rating,

    LAG(white_rating) OVER (
        PARTITION BY white_id
        ORDER BY game_id
    ) AS prev_rating

FROM games;
"""

result = pd.read_sql(query, conn)
print(result)
conn.close()

