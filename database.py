import sqlite3

def init_db():
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        role TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_message(username, role, message):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO chats (username, role, message) VALUES (?, ?, ?)",
        (username, role, message)
    )

    conn.commit()
    conn.close()


def load_messages(username):
    conn = sqlite3.connect("chat_history.db")
    c = conn.cursor()

    c.execute(
        "SELECT role, message FROM chats WHERE username=?",
        (username,)
    )

    rows = c.fetchall()
    conn.close()

    return rows
