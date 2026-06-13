import sqlite3
import pandas as pd


conn = sqlite3.connect("data/chess.db")

query = """
SELECT
    opening_code,
    COUNT(*) AS games
FROM games
GROUP BY opening_code
HAVING COUNT(*) > 500
ORDER BY games DESC
LIMIT 5;
"""

result = pd.read_sql(query, conn)

print(result)

conn.close()


