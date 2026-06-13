import sqlite3
import pandas as pd

conn = sqlite3.connect("data/processed/chess.db")

query = """
SELECT
    COUNT(*) AS never_white_players
FROM players AS p
LEFT JOIN games AS g
    ON p.username = g.white_id
WHERE g.white_id IS NULL;
"""

result = pd.read_sql(query, conn)
print(result)
conn.close()