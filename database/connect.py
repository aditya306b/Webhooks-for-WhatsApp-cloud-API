import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(f"Connected to SQLite database at {db_file}")
    except Error as e:
        print(f"Error connecting to SQLite: {e}")
    return connection

def create_task_table(connection):
    """Create a table in the SQLite database."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        status BOOLEAN default False,
        task TEXT NOT NULL,
        time TEXT

    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        print("Table 'users' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")


def connect_task_db():
    database = "tasks.db"  # SQLite database file
    connection = create_connection(database)
    create_task_table(connection)
    return connection