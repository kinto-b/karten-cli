"""Extract and process Kindle lookups"""

import os
import sqlite3
from datetime import datetime


def kindle_connect(kindle_dir: str) -> sqlite3.Connection:
    """Connect to the Kindle vocab.db"""
    db = os.path.join(kindle_dir, "system", "vocabulary", "vocab.db")
    return sqlite3.connect(db)


def kindle_read(kindle_dir: str, lang: str, date_from: datetime) -> list[str]:
    """Read words from the Kindle vocab.db"""
    timestamp = int(date_from.timestamp() * 1000)

    con = kindle_connect(kindle_dir)
    try:
        cursor = con.cursor()
        cursor.execute(
            "SELECT DISTINCT stem \
            FROM words \
            WHERE lang=? AND timestamp>?\
            ORDER BY timestamp DESC;",
            (lang.lower(), timestamp),
        )

        words = []
        for (word,) in cursor.fetchall():
            words.append(word)
        return words
    finally:
        con.close()
