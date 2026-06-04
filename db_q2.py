import sqlite3
import pandas as pd

conn = sqlite3.connect("data/chess.db")

query = """
SELECT
    victory_status,
    COUNT(*) AS game_count
FROM games
GROUP BY victory_status
"""

result = pd.read_sql(query, conn)

print(result)

conn.close()