import sqlite3
import pandas as pd

conn = sqlite3.connect("data/chess.db")

query = """
SELECT
    COUNT(*) AS total_games,
    SUM(rated) AS rated_games
FROM games
"""

result = pd.read_sql(query, conn)

print(result)

conn.close()