import mysql.connector
import numpy as np
import json
from db import get_db_connection, close_db_connection, execute_query  # Import functions from your helper file


def get_user_submissions(username):
    db, cursor = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = """
    SELECT s.problem_id, s.verdict, p.diff_rating AS rating
    FROM submissions s
    JOIN problems p ON s.problem_id = p.problem_id
    WHERE s.username = %s
    """
    execute_query(cursor, query, (username,))
    submissions = cursor.fetchall()
    close_db_connection(db, cursor)
    
    return submissions


def process_user_data(username):
    submissions = get_user_submissions(username)
    problem_count = 0
    first_attempt_solved = 0
    solved_problems = set()
    problem_ratings = []
    problem_attempts = {}

    for submission in submissions:
        problem_id = submission['problem_id']
        
        if problem_id not in problem_attempts:
            problem_attempts[problem_id] = {'solved': False, 'failed': 0}
        
        if submission['verdict'] == 'Accepted':
            if problem_attempts[problem_id]['failed'] == 0 and not problem_attempts[problem_id]['solved']:
                first_attempt_solved += 1
                problem_attempts[problem_id]['solved'] = True

            problem_rating = submission['rating']
            if problem_rating is not None:
                problem_ratings.append(problem_rating)

            if problem_id not in solved_problems:
                solved_problems.add(problem_id)
                problem_count += 1

        elif submission['verdict'] != 'OK':
            problem_attempts[problem_id]['failed'] += 1

    avg_rating = np.mean(problem_ratings) if problem_ratings else 0
    highest_rating = max(problem_ratings) if problem_ratings else 0
    first_attempt_percentage = (first_attempt_solved / problem_count) * 100 if problem_count else 0

    return {
        "username": username,
        "problem_count": problem_count,
        "average_rating": avg_rating,
        "highest_rating": highest_rating,
        "first_attempt_percentage": first_attempt_percentage
    }

def save_to_json(data, filename="user_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


def main():
    username = "aru123"  
    user_data = process_user_data(username)

    save_to_json(user_data)

    print(f"User ID: {user_data['username']}")
    print(f"Problem Count: {user_data['problem_count']}")
    print(f"Average Rating of Problems Solved: {user_data['average_rating']:.2f}")
    print(f"Highest Rating of Problems Solved: {user_data['highest_rating']}")
    print(f"First Attempt Success Percentage: {user_data['first_attempt_percentage']:.2f}%")

