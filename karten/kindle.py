"""Extract and process Kindle lookups"""

import sqlite3


def kindle_read(vocab_db: str, lang: str) -> set[str]:
    """Read words in a given language from the Kindle vocab.db"""
    con = sqlite3.connect(vocab_db)
    cursor = con.cursor()
    cursor.execute(
        "SELECT DISTINCT stem FROM words WHERE lang=? ORDER BY timestamp DESC;",
        (lang,),
    )

    words = set()
    for (word,) in cursor.fetchall():
        words.add(word)

    return words
