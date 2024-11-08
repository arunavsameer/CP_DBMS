import mysql.connector

def get_db_connection():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="279936",
        database="cpdbs"
    )
    cursor = db.cursor()
    return db, cursor

def close_db_connection(db, cursor):
    cursor.close()
    db.close()

def execute_query(cursor, query, values=None):
    if values:
        # Check if 'values' is a list of tuples for batch inserts
        if isinstance(values, list) and all(isinstance(v, tuple) for v in values):
            cursor.executemany(query, values)
        else:
            cursor.execute(query, values)
    else:
        cursor.execute(query)
