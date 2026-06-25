from core.db_connection import DBConnection
from datetime import date

def create_user(name, weight, height, age, gender, activity_level, objective):
    """Inserts a new user profile registry into the database."""
    query = """
        INSERT INTO User_Data (Name, Body_Weight, Height, Age, Gender, Activity_Level, Objective)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with DBConnection() as (cursor, conn):
        cursor.execute(query, (name, weight, height, age, gender, activity_level, objective))
        conn.commit()
        return cursor.lastrowid

def get_all_users():
    """Fetches a high-level summary of all profiles for the selection screen."""
    query = "SELECT User_ID, Name, Objective FROM User_Data ORDER BY Name ASC"
    with DBConnection() as (cursor, _):
        cursor.execute(query)
        return cursor.fetchall()

def get_user_profile(user_id):
    """Retrieves full biometric parameters for a single user tracking session."""
    query = "SELECT * FROM User_Data WHERE User_ID = %s"
    with DBConnection() as (cursor, _):
        cursor.execute(query, (user_id,))
        return cursor.fetchone()

def sync_daily_record(user_id):
    """
    Checks if a log row exists for the user on the current date.
    If absent, seamlessly initializes a fresh 0-state log entry row.
    """
    today = date.today()
    select_query = "SELECT * FROM Track_Record WHERE User_ID = %s AND Log_Date = %s"
    insert_query = "INSERT INTO Track_Record (User_ID, Log_Date) VALUES (%s, %s)"
    
    with DBConnection() as (cursor, conn):
        cursor.execute(select_query, (user_id, today))
        record = cursor.fetchone()
        
        if not record:
            cursor.execute(insert_query, (user_id, today))
            conn.commit()
            cursor.execute(select_query, (user_id, today))
            record = cursor.fetchone()
            
        return record

def update_daily_nutrient(user_id, nutrient_column, amount):
    """
    Increments a specific nutrient target total for today's tracking record.
    Uses parameterized data safely bounded to prevent query manipulation.
    """
    allowed_columns = {'Calories', 'Protein', 'Carbs', 'Fats', 'Footsteps'}
    if nutrient_column not in allowed_columns:
        raise ValueError(f"Unauthorized database attribute modification: {nutrient_column}")
        
    today = date.today()
    query = f"""
        UPDATE Track_Record 
        SET {nutrient_column} = {nutrient_column} + %s 
        WHERE User_ID = %s AND Log_Date = %s
    """
    with DBConnection() as (cursor, conn):
        cursor.execute(query, (amount, user_id, today))
        conn.commit()

def get_raw_history_logs(user_id, day_limit=7):
    """Pulls structural time-series logs for historical trend rendering."""
    query = """
        SELECT Log_Date, Calories, Protein, Carbs, Fats, Footsteps 
        FROM Track_Record 
        WHERE User_ID = %s 
        ORDER BY Log_Date DESC 
        LIMIT %s
    """
    with DBConnection() as (cursor, _):
        cursor.execute(query, (user_id, day_limit))
        return cursor.fetchall()