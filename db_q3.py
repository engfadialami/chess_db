import sqlite3
import pandas as pd

conn = sqlite3.connect("data/chess.db")

query = """
SELECT
    game_id,
    winner,
    turns
FROM games
ORDER BY turns DESC
LIMIT 10
"""

result = pd.read_sql(query, conn)

print(result)

conn.close()