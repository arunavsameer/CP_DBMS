# sql_scripts/main.py
import sys
from db import get_db_connection, close_db_connection
from user import fetch_and_insert_user_details
from contests import fetch_and_insert_user_submissions

def main(username, email, hashed_password):
    try:
        db, cursor = get_db_connection()
        
        # Start Transaction
        db.start_transaction()
        
        # Insert User Details
        fetch_and_insert_user_details(cursor, db, username, email, hashed_password)
        
        # Insert User Submissions
        fetch_and_insert_user_submissions(cursor, db, username, count=5)
        
        # Commit Transaction
        db.commit()
        print("Database operations completed successfully.")
    except Exception as e:
        # Rollback Transaction in case of error
        db.rollback()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        close_db_connection(db, cursor)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <username> <email> <hashed_password>", file=sys.stderr)
        sys.exit(1)
    username = sys.argv[1]
    email = sys.argv[2]
    hashed_password = sys.argv[3]
    main(username, email, hashed_password)