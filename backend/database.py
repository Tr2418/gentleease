import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "gentleease.db")

def get_connection():
    """Opens a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # So rows come back as dicts
    return conn

def init_db():
    """Creates all tables if they don't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table for generic app settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)

    # Table for medications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meds (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT    NOT NULL,
            time  TEXT    NOT NULL
        )
    """)

    # Table for health records / documents
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            type     TEXT NOT NULL DEFAULT 'General',
            date     TEXT NOT NULL,
            notes    TEXT DEFAULT ''
        )
    """)

    # Table for chat history (optional — stores last 50 messages)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            role      TEXT NOT NULL,
            message   TEXT NOT NULL,
            timestamp TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database ready at:", DB_PATH)
