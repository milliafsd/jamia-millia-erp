import sqlite3

DB="jamia.db"

def connect():

    conn = sqlite3.connect("jamia.DB", check_same_thread=False)

    return conn


def init_db():

    conn=connect()

    c=conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    father TEXT,
    teacher TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    password TEXT
    )
    """)

    conn.commit()

    return conn
