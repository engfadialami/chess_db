import sqlite3
import pandas as pd

conn = sqlite3.connect("data/processed/chess.db")

query = """
WITH player_wins AS (
    SELECT
        white_id AS username,
        COUNT(*) AS wins
    FROM games
    WHERE winner = 'White'
    GROUP BY white_id

    uniON ALL

    SELECT
        black_id AS username,
        COUNT(*) AS wins
    FROM games
    WHERE winner = 'Black'
    GROUP BY black_id
)
SELECT
    username,
    SUM(wins) AS total_wins
FROM player_wins
group BY username
ORDER BY total_wins DESC
LIMIT 1;
"""
# UNION CTE: combine white wins and black wins into one 'player_wins' table. Who has the most total wins?



result = pd.read_sql(query, conn)
print(result)
conn.close()