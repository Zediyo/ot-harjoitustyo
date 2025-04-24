import sqlite3
import json
import constants

conn = None

def get_connection():
    global conn
    #use memory db if not initialized
    if conn is None:
        conn = sqlite3.connect(":memory:")
        create_tables()
    return conn

def close_connection():
    global conn
    if conn is not None:
        conn.close()
        conn = None

def init_db():
    global conn

    if conn is not None:
        conn.close()

    conn = sqlite3.connect("data.db")
    create_tables()

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # cursor.execute("DROP TABLE IF EXISTS level_times")
    # cursor.execute("DROP TABLE IF EXISTS levels")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS level_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level_id integer NOT NULL,
            time REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            data TEXT
        )
    """)

    cursor.execute("SELECT 1 FROM levels WHERE name = ?", ("test_level",))

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO levels (name, data) VALUES (?, ?)
        """, ("test_level", json.dumps(constants.TEST_LEVEL)))

    conn.commit()


def save_level_time(level_id, time):
    if level_id < 0 or time < 0:
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO level_times (level_id, time) VALUES (?, ?)",
        (level_id, time)
    )

    conn.commit()


def get_best_time(level_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MIN(time) FROM level_times WHERE level_id = ?",
        (level_id,)
    )
    result = cursor.fetchone()

    return result[0] if result[0] is not None else -1


def save_level(name, level_data):
    if not isinstance(level_data, list) or len(level_data) == 0:
        return
    
    if not isinstance(level_data[0], list) or len(level_data[0]) == 0:
        return
    
    conn = get_connection()
    data = json.dumps(level_data)

    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO levels (name, data) VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET data = excluded.data
        """,
                   (name, data)
                   )

    conn.commit()


def load_level_data(level_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT data FROM levels WHERE id = ?",
        (level_id,)
    )

    result = cursor.fetchone()

    return json.loads(result[0]) if result is not None else None


def get_all_levels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, data FROM levels ORDER BY id ASC")
    levels = cursor.fetchall()
    return [(level_id, name, json.loads(data)) for (level_id, name, data) in levels]


def get_all_best_times():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT level_id, MIN(time)
        FROM level_times
        GROUP BY level_id
    ''')
    return dict(cursor.fetchall())


def level_name_exists(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM levels WHERE name = ?",
        (name,)
    )
    result = cursor.fetchone()
    return result[0] > 0

def get_level_id(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM levels WHERE name = ?",
        (name,)
    )
    result = cursor.fetchone()
    return result[0] if result is not None else None


def delete_level(level_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM levels WHERE id = ?",
        (level_id,)
    )
    cursor.execute(
        "DELETE FROM level_times WHERE level_id = ?",
        (level_id,)
    )
    conn.commit()


def delete_times(level_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM level_times WHERE level_id = ?",
        (level_id,)
    )
    conn.commit()
