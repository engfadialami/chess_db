import sqlite3
import pandas as pd

conn = sqlite3.connect("data/processed/chess.db")

query = """
SELECT
    g.opening_code,
    o.opening_fullname,
    COUNT(*) AS total_games
FROM games AS g
JOIN openings AS o
    ON g.opening_code = o.opening_code
GROUP BY
    g.opening_code,
    o.opening_fullname
ORDER BY total_games DESC
LIMIT 5;
"""

result = pd.read_sql(query, conn)
print(result)
conn.close()