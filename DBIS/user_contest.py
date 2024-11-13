import mysql.connector
import requests
from mysql.connector import Error
from db import execute_query, get_db_connection, close_db_connection

def fetch_contest_data(username):
    url = f"https://codeforces.com/api/user.rating?handle={username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        print(f"Error fetching data for {username}")
        return None

def insert_contest_data(username, contest_data, cursor, db):
    query = """
    INSERT INTO user_contests (username, contest_id, contest_rank, rating_change, penalty)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = [
        (username, contest['contestId'], contest['rank'], contest['newRating'] - contest['oldRating'], contest.get('penalty', 0))
        for contest in contest_data
    ]

    execute_query(cursor, query, values)
    db.commit()
    print(f"Inserted {len(values)} records for user {username}")
    
def fill_user_contest(usernames):
    db, cursor = get_db_connection()
    try:
        for username in usernames:
            contest_data = fetch_contest_data(username)
            if contest_data:

                for contest in contest_data:
                    contest_id = contest['contestId']  
                    cursor.execute("SELECT 1 FROM contests WHERE contest_id = %s", (contest_id,))
                    if cursor.fetchone():  
                        insert_contest_data(username, [contest], cursor, db)
    finally:
        close_db_connection(db, cursor)



usernames = ["user1", "user2"]  
fill_user_contest(usernames)
