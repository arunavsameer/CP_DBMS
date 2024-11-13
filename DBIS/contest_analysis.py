import mysql.connector
import json
from mysql.connector import Error
from datetime import datetime



db_config = {
    "host": "localhost",
    "user": "root",
    "password": "T@nishq123",
    "database": "cpdbs"
}


def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error: {e}")
        return None


def mysql_datetime_to_str(mysql_datetime):
    if mysql_datetime:
        return mysql_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return None


def get_contest_count_and_best_rank(username):
    db = get_db_connection()
    if db is None:
        return

    try:
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT COUNT(uc.contest_id) AS contest_count, MIN(uc.contest_rank) AS best_rank
            FROM user_contests uc
            WHERE uc.username = %s;
        """
        cursor.execute(query, (username,))
        data = cursor.fetchall()

        for entry in data:
            entry['contest_count'] = int(entry['contest_count'])
            entry['best_rank'] = int(entry['best_rank']) if entry['best_rank'] is not None else None

        with open(f'{username}contest_count_best_rank.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print("Contest count and best rank saved to contest_count_best_rank.json")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_user_rating_history(username):
    db = get_db_connection()
    if db is None:
        return

    try:
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT c.start_time AS contest_date, uc.rating_change, u.rating AS final_rating
            FROM user_contests uc
            JOIN contests c ON uc.contest_id = c.contest_id
            JOIN users u ON uc.username = u.username
            WHERE uc.username = %s
            ORDER BY c.start_time;
        """
        cursor.execute(query, (username,))
        data = cursor.fetchall()

        for entry in data:
            entry['contest_date'] = mysql_datetime_to_str(entry['contest_date'])
            entry['rating_change'] = int(entry['rating_change'])
            entry['final_rating'] = int(entry['final_rating']) if entry['final_rating'] is not None else None

        with open(f'{username}user_rating_history.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print("User rating history saved to user_rating_history.json")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def get_contest_cards(username):
    db = get_db_connection()
    if db is None:
        return

    try:
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT 
                c.contest_name, 
                uc.contest_rank, 
                uc.rating_change, 
                uc.penalty,
                (SELECT COUNT(DISTINCT s.problem_id) 
                FROM submissions s 
                JOIN problems p ON s.problem_id = p.problem_id
                WHERE s.username = uc.username AND p.contest_id = uc.contest_id) AS problems_solved
            FROM 
                user_contests uc
            JOIN 
                contests c ON uc.contest_id = c.contest_id
            WHERE 
                uc.username = %s;

        """
        cursor.execute(query, (username,))
        data = cursor.fetchall()
        print(data)

        for entry in data:
            entry['contest_rank'] = int(entry['contest_rank'])
            entry['rating_change'] = int(entry['rating_change'])
            entry['penalty'] = int(entry['penalty']) if entry['penalty'] is not None else None
            entry['problems_solved'] = int(entry['problems_solved'])

        with open(f'{username}contest_cards.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print("Contest cards saved to contest_cards.json")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    username = "aru123" 
    get_contest_count_and_best_rank(username)
    get_user_rating_history(username)
    get_contest_cards(username)



