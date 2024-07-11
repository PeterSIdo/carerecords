import sqlite3

def create_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('care4.db')
    cursor = conn.cursor()

    # SQL command to create the food_chart table
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS personal_care_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personal_care_name TEXT
    )
    '''

    # Execute the SQL command
    cursor.execute(create_table_sql)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Table created successfully.")