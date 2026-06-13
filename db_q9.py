import sqlite3
import pandas as pd

conn = sqlite3.connect("data/processed/chess.db")

query = """
WITH white_wins AS (
    SELECT
        white_id AS username,
        COUNT(*) AS wins_as_white
    FROM games
    WHERE winner = 'White'
    GROUP BY white_id
)
SELECT
    username,
    wins_as_white
FROM white_wins
ORDER BY wins_as_white DESC
LIMIT 5;
"""

# query = """
# SELECT
#     white_id,
#     COUNT(*)
# FROM games
# WHERE winner='White'
# GROUP BY white_id
# ORDER BY COUNT(*) DESC
# LIMIT 5;
# """


result = pd.read_sql(query, conn)
print(result)
conn.close()