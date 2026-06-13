import os
import sqlite3
import logging

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

log = logging.getLogger(__name__)


RAW_CSV_PATH = os.path.join("data", "raw", "chess_games.csv")
DB_PATH = os.path.join("data", "processed", "chess.db")


def create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("DROP TABLE IF EXISTS games")
    conn.execute("DROP TABLE IF EXISTS openings")
    conn.execute("DROP TABLE IF EXISTS players")

    conn.execute("""
        CREATE TABLE players (
            username TEXT PRIMARY KEY NOT NULL,
            last_rating INTEGER NOT NULL,
            total_games INTEGER NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE openings (
            opening_code TEXT PRIMARY KEY NOT NULL,
            opening_shortname TEXT,
            opening_fullname TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE games (
            game_id INTEGER PRIMARY KEY NOT NULL,
            white_id TEXT NOT NULL,
            black_id TEXT NOT NULL,
            winner TEXT NOT NULL CHECK(winner IN ('White', 'Black', 'Draw')),
            victory_status TEXT NOT NULL,
            turns INTEGER NOT NULL,
            time_increment TEXT,
            rated INTEGER NOT NULL,
            white_rating INTEGER NOT NULL,
            black_rating INTEGER NOT NULL,
            opening_code TEXT NOT NULL,

            FOREIGN KEY (white_id) REFERENCES players(username),
            FOREIGN KEY (black_id) REFERENCES players(username),
            FOREIGN KEY (opening_code) REFERENCES openings(opening_code)
        )
    """)

    log.info("Schema created successfully.")


def prepare_data(chess: pd.DataFrame):
    white = chess[["white_id", "white_rating"]].rename(
        columns={
            "white_id": "username",
            "white_rating": "rating"
        }
    )

    black = chess[["black_id", "black_rating"]].rename(
        columns={
            "black_id": "username",
            "black_rating": "rating"
        }
    )

    players_df = (
        pd.concat([white, black])
        .groupby("username")["rating"]
        .last()
        .reset_index()
        .rename(columns={"rating": "last_rating"})
    )

    white_counts = chess["white_id"].value_counts()
    black_counts = chess["black_id"].value_counts()

    players_df["total_games"] = (
        players_df["username"]
        .map(white_counts.add(black_counts, fill_value=0))
        .astype(int)
    )

    openings_df = (
        chess[
            [
                "opening_code",
                "opening_shortname",
                "opening_fullname"
            ]
        ]
        .drop_duplicates("opening_code")
        .reset_index(drop=True)
    )

    games_df = chess[
        [
            "game_id",
            "white_id",
            "black_id",
            "winner",
            "victory_status",
            "turns",
            "time_increment",
            "rated",
            "white_rating",
            "black_rating",
            "opening_code"
        ]
    ].copy()

    return players_df, openings_df, games_df


def load_data(
    conn: sqlite3.Connection,
    players_df: pd.DataFrame,
    openings_df: pd.DataFrame,
    games_df: pd.DataFrame
) -> None:

    players_df.to_sql(
        "players",
        conn,
        if_exists="append",
        index=False
    )

    openings_df.to_sql(
        "openings",
        conn,
        if_exists="append",
        index=False
    )

    games_df.to_sql(
        "games",
        conn,
        if_exists="append",
        index=False
    )

    log.info(f"Players table: {len(players_df)} rows inserted.")
    log.info(f"Openings table: {len(openings_df)} rows inserted.")
    log.info(f"Games table: {len(games_df)} rows inserted.")


def create_indexes(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_games_white_id
        ON games(white_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_games_black_id
        ON games(black_id)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_games_opening_code
        ON games(opening_code)
    """)
    log.info("Indexes created successfully.")


def verify_schema(conn: sqlite3.Connection) -> None:
    expected = {
        "players": 15635,
        "openings": 365,
        "games": 20058
    }

    for table, expected_rows in expected.items():
        actual = conn.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        assert actual == expected_rows, (
            f"Expected {expected_rows} rows in {table}, got {actual}"
        )

        log.info(f"Verified {table}: {actual} rows.")


def show_query_plan(conn: sqlite3.Connection) -> None:
    plan = conn.execute("""
        EXPLAIN QUERY PLAN
        SELECT *
        FROM games
        WHERE white_id = 'taranga'
    """).fetchall()

    log.info("EXPLAIN QUERY PLAN for white_id search:")
    for row in plan:
        log.info(row)


def main() -> None:
    print("Building Assignment 6 chess database...")

    chess = pd.read_csv(RAW_CSV_PATH)

    log.info(
        f"Loaded chess_games.csv: {chess.shape[0]} rows, {chess.shape[1]} columns."
    )

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    create_schema(conn)

    players_df, openings_df, games_df = prepare_data(chess)

    load_data(conn, players_df, openings_df, games_df)

    create_indexes(conn)

    verify_schema(conn)

    show_query_plan(conn)

    conn.commit()
    conn.close()

    log.info(f"Database created successfully at {DB_PATH}")


if __name__ == "__main__":
    main()