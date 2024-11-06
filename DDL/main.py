from db import get_db_connection, close_db_connection
from user import fetch_and_insert_user_details
from contests import fetch_and_insert_user_submissions

def main():
    db, cursor = get_db_connection()
    user_handles = ['err_hexa', 'aru123', 'tanishqgodha']
    
    fetch_and_insert_user_details(cursor, db, user_handles)
    
    for handle in user_handles:
        fetch_and_insert_user_submissions(cursor, db, handle, count=5)
    
    close_db_connection(db, cursor)
    print("Database operations completed successfully.")

if __name__ == "__main__":
    main()
