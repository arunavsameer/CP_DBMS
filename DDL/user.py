import requests
from db import execute_query

api_url = "https://codeforces.com/api/"

def user_exists(cursor, handle):
    query = "SELECT COUNT(*) FROM users WHERE username = %s"
    cursor.execute(query, (handle,))
    result = cursor.fetchone()
    return result[0] > 0

def get_orgy(organisation):
    return organisation if organisation else None

def fetch_user_problem_count(cursor, handle):
    url_status = f"{api_url}user.status?handle={handle}"
    response_status = requests.get(url_status)
    
    if response_status.status_code == 200:
        submissions = response_status.json()["result"]
        unique_solved_problems = {
            (submission["problem"]["contestId"], submission["problem"]["index"])
            for submission in submissions if submission["verdict"] == "OK"
        }
        return len(unique_solved_problems)
    else:
        print(f"Failed to fetch submissions for user {handle}. Status code: {response_status.status_code}")
        return 0

def fetch_and_insert_user_details(cursor, db, user_handles):
    handles = ";".join(user_handles)
    
    url_info = f"{api_url}user.info?handles={handles}"
    response_info = requests.get(url_info)
    
    if response_info.status_code == 200:
        users = response_info.json()["result"]
        
        for user in users:
            if not user_exists(cursor, user["handle"]):
                problem_count = fetch_user_problem_count(cursor, user["handle"])
                
                query = """
                INSERT INTO users (username, email, rating, country, university, problem_count, max_rating, rating_title)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    email = VALUES(email),
                    rating = VALUES(rating),
                    country = VALUES(country),
                    university = VALUES(university),
                    problem_count = VALUES(problem_count),
                    max_rating = VALUES(max_rating),
                    rating_title = VALUES(rating_title)
                """
                values = (
                    user["handle"],
                    None,
                    user.get("rating"),
                    user.get("country"),
                    get_orgy(user.get("organization")),
                    problem_count,
                    user.get("maxRating"),
                    user.get("rank")
                )
                execute_query(cursor, query, values)
                db.commit()
                print(f"User details for {user['handle']} added/updated successfully.")
            else:
                print(f"User {user['handle']} already exists in the database.")
    else:
        print(f"Failed to fetch user details. Status code: {response_info.status_code}")
