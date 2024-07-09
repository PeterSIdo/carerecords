import sqlite3

def create_staff_initials_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()
    
    # SQL command to create the staff_initials table
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS staff_initials (
        id INTEGER PRIMARY KEY,
        staff_name TEXT,
        staff_surname TEXT,
        staff_initials TEXT
    )
    '''
    
    # Execute the SQL command
    cursor.execute(create_table_sql)
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to create the table
create_staff_initials_table()