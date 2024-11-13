from db import get_db_connection, close_db_connection
from user import fetch_and_insert_user_details
from contests import fetch_and_insert_user_submissions 
from user_contest import fill_user_contest
from contest_analysis import get_contest_cards,get_contest_count_and_best_rank,get_user_rating_history
from problem_anal import process_user_data,save_to_json

def main():
    db, cursor = get_db_connection()
    user_handles = ['err_hexa', 'aru123', 'tanishqgodha',"anmoljoshicrx128"]
    
    fetch_and_insert_user_details(cursor, db, user_handles)
    
    for handle in user_handles:
        fetch_and_insert_user_submissions(cursor, db, handle, count=25)
        
    fill_user_contest(user_handles)
    
    # for handle in user_handles:
    #     get_user_rating_history(handle)
    #     get_contest_cards(handle)
    #     get_contest_count_and_best_rank(handle)
    #     user_data = process_user_data(handle)
    #     save_to_json(user_data, filename=f"{handle}.json")
    
    close_db_connection(db, cursor)
    print("Database operations completed successfully.")

if __name__ == "__main__":
    main()
