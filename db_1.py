import sqlite3
import pandas as pd

conn = sqlite3.connect("data/chess.db")

df = pd.read_sql("SELECT * FROM games LIMIT 5", conn)

print(df.columns.tolist())