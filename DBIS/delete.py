import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="T@nishq123",
    database="cpdbs"
)
cursor = db.cursor()

tables = [
    "submissions",
    "problem_tags",
    "tags",
    "problems",
    "user_contests",
    "contest_authors",
    "contests",
    "users"
]


for table in tables:
    try:
        cursor.execute(f"DELETE FROM {table}")
        print(f"All data deleted from {table}.")
    except mysql.connector.Error as err:
        print(f"Error deleting data from {table}: {err}")

db.commit()
cursor.close()
db.close()
