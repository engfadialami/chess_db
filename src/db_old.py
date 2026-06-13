import os
import sqlite3
import logging

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

log = logging.getLogger(__name__)


def build_tables(conn: sqlite3.Connection,
                 chess: pd.DataFrame) -> None:

    # --------------------------------------------------
    # PLAYERS TABLE
    # --------------------------------------------------

    white = chess[
        ["white_id", "white_rating"]
    ].rename(
        columns={
            "white_id": "username",
            "white_rating": "rating"
        }
    )

    black = chess[
        ["black_id", "black_rating"]
    ].rename(
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
        .map(
            white_counts.add(
                black_counts,
                fill_value=0
            )
        )
        .astype(int)
    )

    players_df.to_sql(
        "players",
        conn,
        if_exists="replace",
        index=False
    )

    log.info(
        f"Players table: {len(players_df)} rows have been created."
    )

    # --------------------------------------------------
    # OPENINGS TABLE
    # --------------------------------------------------

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

    openings_df.to_sql(
        "openings",
        conn,
        if_exists="replace",
        index=False
    )

    log.info(
        f"Openings table: {len(openings_df)} rows have been created."
    )

    # --------------------------------------------------
    # GAMES TABLE
    # --------------------------------------------------

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

    games_df.to_sql(
        "games",
        conn,
        if_exists="replace",
        index=False
    )

    log.info(
        f"Games table: {len(games_df)} rows have been created."
    )

    # --------------------------------------------------
    # INDEXES
    # --------------------------------------------------

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_games_white
        ON games(white_id)
        """
    )

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_games_black
        ON games(black_id)
        """
    )

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_games_opening
        ON games(opening_code)
        """
    )

    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_games_winner
        ON games(winner)
        """
    )

    log.info(
        "Indexes on games table have been created."
    )


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
            f"Expected {expected_rows} rows in "
            f"{table}, got {actual}"
        )

        log.info(
            f"Verified {table} table: "
            f"{actual} rows."
        )


def main():

    print("This is for Session 6: testing databases")

    chess = pd.read_csv(
        os.path.join(
            "data",
            "raw",
            "chess_games.csv"
        )
    )

    print(
        f"Loaded chess_games.csv: "
        f"{chess.shape[0]} rows, "
        f"{chess.shape[1]} columns."
    )

    db_path = os.path.join(
        "data",
        "processed",
        "chess.db"
    )

    conn = sqlite3.connect(db_path)

    build_tables(conn, chess)

    verify_schema(conn)

    conn.commit()

    log.info(
        f"Database tables have been built. "
        f"{os.path.getsize(db_path)/1024:.2f} KB"
    )

    conn.close()


if __name__ == "__main__":
    main()