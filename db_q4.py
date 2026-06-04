import sqlite3
import pandas as pd

conn = sqlite3.connect("data/chess.db")

query = """
SELECT
    winner,
    COUNT(*) AS game_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM games), 2) AS win_rate_percent
FROM games
GROUP BY winner
ORDER BY win_rate_percent DESC
"""

result = pd.read_sql(query, conn)

print(result)

conn.close()