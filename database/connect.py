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

def create_table(connection):
    """Create a table in the SQLite database."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        status TEXT,
        task TEXT UNIQUE
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        print("Table 'users' created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")

# def insert_user(connection, user):
#     """Insert a user into the users table."""
#     insert_sql = """
#     INSERT INTO users (name, age, email)
#     VALUES (?, ?, ?);
#     """
#     try:
#         cursor = connection.cursor()
#         cursor.execute(insert_sql, user)
#         connection.commit()
#         print(f"User {user[0]} added successfully.")
#     except Error as e:
#         print(f"Error inserting user: {e}")

# def fetch_users(connection):
#     """Fetch all users from the users table."""
#     fetch_sql = "SELECT * FROM users;"
#     try:
#         cursor = connection.cursor()
#         cursor.execute(fetch_sql)
#         rows = cursor.fetchall()
#         print("Users:")
#         for row in rows:
#             print(row)
#     except Error as e:
#         print(f"Error fetching users: {e}")

def connect_db():
    database = "project.db"  # SQLite database file
    connection = create_connection(database)
    create_table(connection)
    return connection