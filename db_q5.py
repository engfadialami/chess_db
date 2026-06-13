import sqlite3
import pandas as pd


conn = sqlite3.connect("data/chess.db")

query = """
SELECT
    victory_status,
    ROUND(AVG(turns), 1) AS avg_turns,
    MAX(turns) AS max_turns
FROM games
GROUP BY victory_status
ORDER BY avg_turns DESC;
"""

result = pd.read_sql(query, conn)

print(result)

conn.close()